import argparse
import json
import logging
import os
import sys
import tempfile
from datetime import datetime

import openai
from . import train
from . import local_metadata_store as lms
from .planner import Planner, SyncPlanner
from openai import error

from .event_logger import log_event
from .local_events_cache import cached_events_iter

# logger = logging.getLogger(__name__)
logger = logging.getLogger("openai_finetune.cli")
formatter = logging.Formatter("[%(asctime)s] %(message)s")
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)


def verify_files_exist(urls):
    # TODO
    pass


def finetune(args):
    train_paths = args.train.split(",")
    val_paths = args.val.split(",") if args.val else []
    verify_files_exist(train_paths + val_paths)

    hps = train.FinetuningHps(
        train_paths=train_paths,
        val_paths=val_paths,
        update_scale=args.scale,
        max_tokens=args.max_tokens,
        num_epochs=args.num_epochs,
        train_batch_size=args.batch_size,
        val_batch_size=args.val_batch_size,
        completions_every=args.completions_every,
        num_completions=args.num_completions,
        completion_temperature=args.completion_temperature,
        completion_tokens=args.completion_tokens,
        completion_prompt=args.completion_prompt,
        snapshots_every=args.snapshots_every,
        pack_context=args.pack_context,
        pack_overlap=args.pack_overlap,
        terminator=args.terminator,
        terminator_weight=args.terminator_weight,
        classification=args.classification,
    )

    if args.engine:
        finetune_sync(args, hps)
    else:
        finetune_async(args, hps)


def finetune_sync(args, hps):
    logger.info(f"Preparing fine-tuning run on engine={args.engine} model={args.model}")
    planner = SyncPlanner(engine=args.engine, model=args.model, encoding=args.encoding)
    train.train(planner=planner, hps=hps)
    planner.close()


def finetune_async(args, hps):
    run = finetune_batch_job(
        hps,
        model=args.model,
        plan_output_file=args.plan_output_file,
        plan_description=args.description,
        plan_id=args.plan,
        encoding=args.encoding,
    )
    if run is not None:
        if args.stream:
            logger.info(
                f"Waiting on progress. Resume any time: openai api events.list -r {run.id} -s"
            )
            # streaming back results with simple pretty-printing
            for event in cached_events_iter(run.id):
                log_event(event["data"], run.id)
        else:
            logger.info(
                f"You can monitor its progress: openai api events.list -r {run.id} -s"
            )


def finetune_batch_job(
    hps,
    *,
    model=None,
    plan_output_file=None,
    plan_description=None,
    plan_id=None,
    encoding="byte-pair-encoding-v0",
):
    create_run = model is not None
    create_plan = plan_id is None

    if create_plan:
        logger.info(f"Fine-tuning model {model} with hps {hps}")
        planner = Planner(encoding=encoding, output=plan_output_file)
        if plan_output_file is None:
            logger.info(
                f"Building plan in tempfile: {planner.file.name} (pass -o <file> to save to disk)."
            )
        else:
            logger.info(
                f"Building plan in {planner.file.name} and will output to {plan_output_file}"
            )

        logger.info(
            f"Building fine-tuning plan. Each line will have at most {hps.max_tokens} tokens, "
            + f"each training batch will have {hps.train_batch_size} examples, "
            + f"and each validation batch will have at most {hps.val_batch_size} examples"
        )
        train.train(
            planner=planner, hps=hps,
        )

        try:
            logger.info(f"Uploading file to create plan object...")
            planner.file.seek(0)
            file = create_openai_file(purpose="plan", file=planner.file)
            plan = openai.Plan.create(
                description=plan_description or "Plan from openai fine-tune",
                file=file.id,
            )
            lms.save(plan.id, planner.metadata)
            logger.info(f"Plan created: {plan}")
            plan_id = plan.id
        finally:
            planner.close()
    if plan_output_file:
        logger.info(f"Plan contents are available in {plan_output_file}")

    if create_run:
        run = openai.Run.create(model=model, plan=plan_id)
        print(
            f"Created run {run.id} from plan {plan_id} with model {model}. You can now interrupt this job, and continue listening to events later via `openai-ft-events -r {run.id}`"
        )
        logger.debug("Run contents: {run}")
    elif create_plan:
        print(
            f"You can now start any number of runs with your plan. For example, run this to fine-tune ada: openai-ft -p {plan.id} -m ada"
        )
    else:
        raise NotImplementedError(
            "Starting multiple runs with the same plan is not supported yet! Or maybe you forgot to specify the model (-m argument)? "
        )

    return run if create_run else None


def add_finetuning_args(sub, override_defaults=None):
    override_defaults = override_defaults or {}
    sub.add_argument(
        "-t", "--train", help="Comma-separated list of files to train on", default=""
    )
    sub.add_argument("--val", help="Comma-separated list of files to evaluate on")
    sub.add_argument("--log-path", help="Directory to write logs to")
    sub.add_argument(
        "--num-epochs",
        default=1,
        type=int,
        help="The number of epochs to run over training set.",
    )
    sub.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="How many examples to have in each step.",
    )
    sub.add_argument(
        "--val-batch-size",
        type=int,
        default=50,
        help="How many examples to have in each val step.",
    )
    sub.add_argument(
        "-s",
        "--scale",
        type=float,
        help="How much to scale the update size by",
        default=1,
    )
    sub.add_argument(
        "--max-tokens",
        type=int,
        help="Set the max number of tokens in each training example",
        default=2048,
    )
    sub.add_argument(
        "--encoding",
        help="Set the encoding used in this plan",
        default="byte-pair-encoding-v0",
    )
    sub.add_argument(
        "--completions-every",
        help="Generate completions every COMPLETIONS_EVERY fine-tuning steps. Use -1 to not generate completions throughout training. Default: %(default)s",
        type=int,
        default=100,
    )
    sub.add_argument(
        "--num-completions",
        help="Generatate this many completions each time completions are generated. Default: %(default)s",
        type=int,
        default=5,
    )
    sub.add_argument(
        "--completion-tokens",
        help="Generatate this many tokens per completion. Default: %(default)s",
        type=int,
        default=128,
    )
    sub.add_argument(
        "--completion-temperature",
        help="Generatate this many tokens per completion. Default: %(default)s",
        type=float,
        default=0.4,
    )
    sub.add_argument(
        "--completion-prompt", help="Prompt for completions", type=str, default=""
    )
    sub.add_argument(
        "--snapshots-every",
        help="Save snapshots every SNAPSHOTS_EVERY fine-tuning steps. Default: %(default)s",
        type=int,
        default=100,
    )

    # API options
    sub.add_argument("--output", help="Save fine-tuning file to a local path")
    sub.add_argument("-d", "--description", help="A description for the Plan")
    sub.add_argument(
        "--plan",
        "-p",
        help="Plan id (start a job using this plan instead of creating a new plan)",
    )
    sub.add_argument("-m", "--model", help="What model to run with")
    sub.add_argument(
        "-e", "--engine", help="What engine to run with (will run synchronously)"
    )
    sub.add_argument(
        "--no-stream",
        dest="stream",
        action="store_false",
        help="Whether to stream back results",
    )
    sub.add_argument(
        "--no-pack-context",
        dest="pack_context",
        action="store_false",
        default=True,
        help="Disable packing multple samples into the context (enabled by default). "
        "Packing into context allows batch size to be roughly constant (which helps "
        "optimization, and makes use of hardware more efficiently). "
        "Disable only when you have a strong reason to.",
    )

    sub.add_argument(
        "--pack-overlap",
        default=-1,
        type=int,
        help="When packing context, this parameter determines what to do with the samples "
        "that did not fit into the context. When 0 or above, the next sample in the "
        "minibatch will start `overlap` prior to where previous sample ended. "
        "When negative, the cut-off part of the sample will be discarded (default). "
        "Positive values are useful when dealing with strings longer than max context size - "
        "these strings will be sliced with overlap.",
    )
    sub.add_argument(
        "--terminator",
        default="<|endoftext|>",
        help="Add this to the end of the sample. Needed when generating completions of varying length. "
        "Do not use for classification etc when completion has a fixed length, or when terminator tokens "
        " are explicitly present in the data. Set to '' to disable. Default: %(default)s",
    )

    sub.add_argument(
        "--terminator-weight",
        default=1.0,
        type=float,
        help="Loss weight of the terminator (see explanation for --terminator). Default: %(default)s",
    )

    sub.add_argument(
        "--classification",
        "-c",
        default=False,
        action="store_true",
        help="Fine-tune for classification - changes some defaults and data processing settings",
    )

    sub.add_argument(
        "--plan-output-file", default=None, type=str,
    )
    sub.set_defaults(func=finetune, **override_defaults)


def add_openai_args(parser):
    parser.add_argument("-b", "--api-base", help="What API base url to use.")
    parser.add_argument("-k", "--api-key", help="What API key to use.")
    parser.add_argument(
        "-o",
        "--organization",
        help="Which organization to run as (will use your default organization if not specified)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        dest="verbosity",
        default=0,
        help="Set verbosity.",
    )


def configure_openai(args):
    if args.api_key is not None:
        openai.api_key = args.api_key
    if args.api_base is not None:
        openai.api_base = args.api_base
    if args.organization is not None:
        openai.organization = args.organization
    openai.max_network_retries = 5

    if args.verbosity == 1:
        logger.setLevel(logging.INFO)
    elif args.verbosity >= 2:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARN)

    logging.getLogger("openai_finetune").setLevel(
        min(logging.WARN, logger.getEffectiveLevel())
    )
    logging.getLogger("openai").setLevel(min(logging.WARN, logger.getEffectiveLevel()))


def create_openai_file(purpose, file):
    # hack to allow upload of large files - our version with requests seems to fail
    # ideally, should be just this:
    #
    # return openai.File.create(purpose="plan", file=planner.file)
    import subprocess

    assert hasattr(
        file, "name"
    ), f"{file} is not a named file - need to be to use curl for upload"
    cmd = [
        "curl",
        "-H",
        "Content-Type: multipart/form-data",
        "-H",
        f"Authorization: Bearer {openai.api_key}",
        "-F",
        f"purpose={purpose}",
        "-F",
        f"file=@{file.name}",
        "-#",
        "--http1.1",
        f"{openai.api_base}/v1/files",
    ]
    logger.debug(f"Running cmd\n{cmd}")
    curl_output = subprocess.check_output(cmd)
    try:
        response = json.loads(curl_output)
    except json.decoder.JSONDecodeError:
        raise ValueError(f"curl retured an error: output {curl_output}")
    return openai.File(id=response["id"])


def main():
    parser = argparse.ArgumentParser(
        description="Run a fine-tuning job using OpenAI finetuning API"
    )
    add_openai_args(parser)
    add_finetuning_args(parser)
    args = parser.parse_args()
    configure_openai(args)
    finetune(args)


if __name__ == "__main__":
    main()
