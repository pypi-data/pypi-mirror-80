import os
import sys
import openai
import argparse
from . import event_logger
from .cli import configure_openai, add_openai_args
from io import BytesIO
import base64
import nbformat as nbf
import matplotlib.pyplot as plt
import numpy as np
import itertools
from io import StringIO
import contextlib
from datetime import datetime
from .local_events_cache import cached_events_iter


class EventSaver:
    # TODO maybe convert this into a wrapper pattern instead of callbacks?
    def __init__(self):
        self.updates = []
        self.completions = []
        self.snapshots = []
        self.run_metadata = None
        self.step_counter = 0

    def update_callback(self, data):
        self.updates.append(data)
        self.step_counter += 1

    def completion_callback(self, data):
        self.completions.append(data)

    def val_batch_callback(self, data):
        self.val_batches.append(data)

    def header_callback(self, data):
        self.run_metadata = data

    def snapshot_callback(self, data):
        self.snapshots.append((self.step_counter - 1, data["id"]))

    def install_callbacks(self, run):
        event_logger.add_update_callback(self.update_callback, run)
        event_logger.add_completion_callback(self.completion_callback, run)
        event_logger.add_callback("log_header", self.header_callback, run)
        event_logger.add_callback("log_snapshot", self.snapshot_callback, run)


update_variables = ["epoch", "val_loss", "val_acc", "loss", "val_labels"]


def choose_template_file(report_data):
    if "val_stats" not in report_data:
        template_file = "report_gen.ipynb"
    elif len(report_data["val_stats"]) == 2:
        template_file = "report_binary.ipynb"
    else:
        template_file = "report_multiclass.ipynb"
    return os.path.join(os.path.dirname(__file__), template_file)


def prepare_report_data(run, event_saver):
    updates = event_saver.updates
    completions = event_saver.completions
    report_data = {
        k: [u[k] for u in updates] for k in update_variables if k in updates[0]
    }
    report_data["run"] = run
    report_data["plan"] = event_saver.run_metadata["created_by"]["plan"]
    report_data["steps"] = list(range(len(report_data["loss"])))
    report_data["snapshots"] = event_saver.snapshots
    report_data["hps"] = event_saver.run_metadata.get("hps")
    report_data["train_stats"] = event_saver.run_metadata.get("train_dataset_stats")
    report_data["val_stats"] = event_saver.run_metadata.get("val_dataset_stats")
    report_data["created"] = event_saver.run_metadata.get("created")

    if "val_labels" in report_data:
        val_labels = []
        val_predictions = []
        label_set = set([])
        for u in updates:
            logprobs = np.array(u["val_data"]["logprobs"])
            masks = np.array(u["val_data"]["mask"])
            logprobs = logprobs[masks >= 1.0].tolist()
            labels = list(zip(u["val_labels"], logprobs))
            val_labels.append(labels)
            label_set.update(u["val_labels"])
            val_predictions.append(u["val_predictions"])
            # val_predictions.append([[(k,v) for k,v in p if k in label_set] for p in u["val_predictions"]])
        report_data["val_labels"] = val_labels
        report_data["val_predictions"] = val_predictions
    return report_data


@contextlib.contextmanager
def capture_stdout(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def produce_notebook(run, report_data):
    template_file = choose_template_file(report_data)
    nb = nbf.read(template_file, nbf.NO_CONVERT)
    for cell in nb["cells"]:
        if "#__insert_run_data" in cell["source"] or cell["cell_type"] != "code":
            cell["source"] = cell["source"].format(**report_data)
        if cell["cell_type"] == "code":
            with capture_stdout() as cell_out:
                exec(cell["source"], locals())
            cell_out = cell_out.getvalue()
            if cell_out:
                cell["outputs"].append(
                    nbf.v4.new_output(
                        output_type="display_data", data={"text/plain": cell_out}
                    )
                )
            if plt.gcf().get_axes():
                pngbuf = BytesIO()
                plt.savefig(pngbuf)
                plt.clf()
                fig_cell = nbf.v4.new_output(
                    output_type="display_data",
                    data={
                        "image/png": base64.b64encode(pngbuf.getvalue()).decode("ascii")
                    },
                )
                cell["outputs"].append(fig_cell)
            # TODO add text output?
    created_human_readable = datetime.fromtimestamp(report_data["created"]).strftime(
        "%Y%m%d_%H%M%S"
    )
    filename = f"run-{created_human_readable}-{run}.ipynb"
    nbf.write(nb, filename)


def run2jupyter(args):
    es = EventSaver()
    run = args.run
    es.install_callbacks(run)
    events_it = cached_events_iter(run)
    # events_it = openai.Event.list(run=run, stream=True, limit=1)
    # TODO add run create time for better ordering in the folder
    for step_idx, event in enumerate(events_it):
        event_logger.log_event(event["data"], run)
        if step_idx > 0 and args.update_every > 0 and step_idx % args.update_every == 0:
            produce_notebook(run, prepare_report_data(run, es))
    produce_notebook(run, prepare_report_data(run, es))


def add_events_args(parser):
    parser.add_argument("--run", "-r", required=True, help="Run id")
    parser.add_argument(
        "--update-every",
        "-u",
        default=-1,
        help="Update notebook every this many steps. Set to negative value to update only after processing the entire run. Default: -1",
        type=int,
    )


def main():
    parser = argparse.ArgumentParser(
        description="List the events for a batch-mode fine-tuning run"
    )
    add_events_args(parser)
    add_openai_args(parser)
    args = parser.parse_args()
    configure_openai(args)
    run2jupyter(args)


if __name__ == "__main__":
    main()
