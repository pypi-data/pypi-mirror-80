import logging
import os.path as osp
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional
from collections import defaultdict
import openai

from .load_dataset import load_dataset, Sampler
from . import data_streams

logger = logging.getLogger(__name__)


@contextmanager
def scoped_log(message):
    tstart = time.time()
    print(f"▕▔ {message}")
    yield
    print(f"▕▁ Done in {time.time()-tstart:.2f} seconds")


@dataclass
class FinetuningHps:
    train_paths: list
    val_paths: list
    num_epochs: int = 1
    train_batch_size: int = 32
    val_batch_size: int = 50
    max_tokens: int = 2048
    update_scale: float = 1.0
    create_plan: bool = True
    plan_output_file: Optional[str] = None
    completions_every: int = 5
    num_completions: int = 1
    completion_tokens: int = 128
    completion_temperature: float = 0.4
    completion_prompt: str = ""
    snapshots_every: int = 100
    pack_context: bool = True
    pack_overlap: int = -1
    terminator: str = "<|endoftext|>"
    terminator_weight: float = 1.0
    val_epochs: bool = False
    classification: bool = False


def get_train_val_it(enc, hps, iepoch, infinite_val_iterator=True):
    assert len(hps.train_paths) > 0
    assert len(hps.val_paths) > 0, "please provide validation data"
    stream_kwargs = dict(
        tokens_per_example=hps.max_tokens,
        enc=enc,
        pack_context=hps.pack_context,
        pack_overlap=hps.pack_overlap,
        terminator=hps.terminator,
        terminator_weight=hps.terminator_weight,
    )
    train_it = data_streams.stream_from_files(
        hps.train_paths,
        **stream_kwargs,
        batch_size=hps.train_batch_size,
        seed=iepoch,
        pad=True,
    )
    val_it = data_streams.stream_from_files(
        hps.val_paths,
        **stream_kwargs,
        batch_size=hps.val_batch_size,
        seed=iepoch,
        pad=False,
        allow_partial_batch=True,
        forever=infinite_val_iterator,
    )
    return train_it, val_it


def flatten(lst):
    return [el for l in lst for el in l]


def classification_dataset_stats(enc, it):
    label_count = defaultdict(int)
    for batch in it:
        tokens = flatten(batch["tokens"])
        mask = flatten(batch["mask"])
        for t, m in zip(tokens, mask):
            if m >= 1.0:
                label_count[t] += 1
    return {enc.decode([k]): v for k, v in label_count.items()}


def train(planner, hps):
    enc = planner.make_encoding()
    step_idx = 0
    plan_metadata = {"hps": hps.__dict__}
    if hps.classification:
        train_it, val_it = get_train_val_it(enc, hps, 0, infinite_val_iterator=False)
        plan_metadata["train_dataset_stats"] = classification_dataset_stats(
            enc, train_it
        )
        plan_metadata["val_dataset_stats"] = classification_dataset_stats(enc, val_it)
    planner.add_plan_metadata(plan_metadata)
    for iepoch in range(hps.num_epochs):
        train_it, val_it = get_train_val_it(enc, hps, iepoch)
        assert (
            step_idx > 0 or iepoch == 0
        ), "one full epoch over data produced no valid training steps, training is not running! Try decreasing the batch size"
        decayed_scale = hps.update_scale * (1 - iepoch / hps.num_epochs)

        def post_val_batch():
            val_batch = next(val_it)
            planner.add(
                "POST /v1/completions",
                prompt=val_batch["tokens"],
                metadata=dict(
                    mask=val_batch["mask"], epoch=iepoch, type="validation_step"
                ),
                logprobs=0 if not hps.classification else 1,
                max_tokens=0,
                echo=True,
            )

        with scoped_log(f"Running epoch: {iepoch}"):
            # Post an extra validation batch at the beginning of the epoch
            # to tell logger that validation data is present (if it is present)
            post_val_batch()
            for batch in train_it:
                if (
                    hps.completions_every > 0
                    and hps.num_completions > 0
                    and step_idx % hps.completions_every == 0
                ):
                    ### Sampling eval
                    planner.add(
                        "POST /v1/completions",
                        n=hps.num_completions,
                        max_tokens=hps.completion_tokens,
                        temperature=hps.completion_temperature,
                        prompt=hps.completion_prompt,
                        echo=True,
                    )

                if (
                    hps.snapshots_every > 0
                    and step_idx > 0
                    and step_idx % hps.snapshots_every == 0
                ):
                    planner.add(
                        "POST /v1/snapshots",
                        description=f"Step {step_idx} of openai-finetune",
                    )
                    val_epoch(planner, hps, iepoch)
                # Training batch
                # TODO in-epoch update_scale planner, probably cosine
                planner.add(
                    "POST /v1/updates",
                    example=batch["tokens"],
                    mask=batch["mask"],
                    scale=decayed_scale,
                )
                post_val_batch()
                step_idx += 1
            planner.flush_to()
        val_epoch(planner, hps, iepoch)
    planner.add(
        "POST /v1/snapshots",
        description=f"Step {step_idx} (last of the training run) of openai-finetune",
    )
    planner.flush_to()


def val_epoch(planner, hps, iepoch):
    if not hps.val_epochs:
        return
    enc = planner.make_encoding()
    _, val_it = get_train_val_it(enc, hps, iepoch, infinite_val_iterator=False)
    for val_batch in val_it:
        planner.add(
            "POST /v1/completions",
            prompt=val_batch["tokens"],
            metadata=dict(
                mask=val_batch["mask"], epoch=iepoch, type="validation_epoch_step"
            ),
            logprobs=0,
            max_tokens=0,
            echo=True,
        )


def save_snapshot(planner, epoch):
    planner.add("POST /v1/snapshots", description=f"Epoch {epoch} of openai-finetune")
