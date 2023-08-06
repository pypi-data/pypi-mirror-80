import numpy as np
import time
from datetime import datetime
from . import local_metadata_store as lms
import openai


def get_run_object(run_id):
    runs = [r for r in openai.Run.list()["data"] if r.id == run_id]
    assert len(runs) == 1
    return runs[0]


class EventLogger:
    def __init__(self, run=None):
        self.run = run
        self.plan_lines = None
        self.metadata = {}
        if run is not None:
            run_object = get_run_object(run)
            self.plan_lines = run_object.total_lines
            self.metadata = lms.load(run_object.plan)
        self.updates_after_header = 0
        self.created = time.time()
        self.val_data_present = False
        self.update_data = None
        self.total_tokens = 0
        self.last_update_time = time.time()

    def log_event(self, data, params=None):
        params = params or {}
        if "error" in data:
            from .cli import logger

            logger.error(data["error"])
            raise ValueError(data["error"])
        if self.run is not None:
            line_idx = data["created_by"]["lineno"]
            metadata = self.metadata.get(str(line_idx), {})
        else:
            metadata = params.get("metadata", {})
        data.update(metadata)
        if data["object"] == "headers":
            self.log_header(data)
        elif data["object"] == "text_completion":
            if metadata.get("type") == "validation_step":
                self.log_val_batch(data)
            elif metadata.get("type") == "validation_epoch":
                self.log_val_epoch_batch(data)
            else:
                self.log_completion(data)
        elif data["object"] == "snapshot":
            self.log_snapshot(data)
        elif data["object"] == "update":
            self.log_update_raw(data)
        else:
            raise ValueError(f"Unknown event type: {data['object']}")

    def log_header(self, data):
        print(
            f"Run {data['created_by']['run']} started from {data['created_by']['plan']} at {datetime.fromtimestamp(data['created'])}"
        )
        self.updates_after_header = 0
        self.total_tokens = 0
        self.created = data["created"]
        self.last_update_time = self.created
        data.update(self.metadata.get("null", {}))

    def log_completion(self, data):
        print("Completions:")
        for choice in data["choices"]:
            print(f"---\n{choice['text']}")
        self.updates_after_header = 0

    def log_val_epoch_batch(self, data):
        raise NotImplementedError

    def log_val_batch(self, data):
        self.val_data_present = True
        if self.update_data is not None:
            update_data = self.update_data
            logprobs = []
            tokens = []
            masks = []
            for choice in data["choices"]:
                logprobs += choice["logprobs"]["token_logprobs"][1:]
                tokens += choice["logprobs"]["tokens"][1:]

            if "mask" in data and "top_logprobs" in data["choices"][0]["logprobs"]:
                labels = []
                predictions = []
                for mask, choice in zip(data["mask"], data["choices"]):
                    label_idx = [i for i, m in enumerate(mask) if m >= 1.0]
                    labels += [choice["logprobs"]["tokens"][i] for i in label_idx]
                    if choice["logprobs"]["top_logprobs"] is not None:
                        predictions += [
                            choice["logprobs"]["top_logprobs"][i] for i in label_idx
                        ]
                update_data["val_labels"] = labels
                update_data["val_predictions"] = predictions
                # Top-k accuracy - compare the label with the most likely prediction
                update_data["val_acc"] = len(
                    [1 for l, p in zip(labels, predictions) if l in p]
                ) / len(labels)

            logprobs = np.array(logprobs)
            if data.get("mask") is not None:
                mask = np.array([m for masks in data["mask"] for m in masks[1:]])
            data["logprobs"] = logprobs
            data["mask"] = mask
            data["tokens"] = tokens
            masked_logprobs = logprobs * mask
            update_data["val_loss"] = -masked_logprobs.sum() / np.sum(mask > 0)

            update_data["epoch"] = data["epoch"]
            update_data["val_data"] = data
            self.log_update(update_data)
        self.update_data = None

    def log_update_raw(self, data):
        data["elapsed"] = data["created"] - self.created
        self.total_tokens += data["tokens"]
        data["total_tokens"] = self.total_tokens
        data["tokens/s"] = data["tokens"] / (data["created"] - self.last_update_time)
        self.last_update_time = data["created"]
        if self.run is not None:
            # used as a run event reader (not in sync mode finetuning)
            data["plan_line"] = data["created_by"]["lineno"]
            data["completed"] = data["created_by"]["lineno"] / self.plan_lines
        data["loss"] = -data["loss"]
        if not self.val_data_present:
            # if no val data, print log lines on update
            # otherwise, on val batch so that val loss
            # is measured after train loss
            self.log_update(data)
        self.update_data = data

    def log_update(self, data):
        keys = [
            "epoch",
            "elapsed",
            "loss",
            "val_loss",
            "scale",
            "tokens",
            "total_tokens",
            "tokens/s",
        ]
        if "plan_line" in data:
            keys += [
                "plan_line",
                "completed",
            ]
        if self.updates_after_header % 10 == 0:
            print(f"\n{' | '.join([k.rjust(12) for k in keys])}")
        print(" | ".join(fixed_width(data.get(k)) for k in keys))
        self.updates_after_header += 1

    def log_snapshot(self, data):
        print(f"Created snapshot {data['id']}")
        self.updates_after_header = 0


def fixed_width(v, width=12):
    if isinstance(v, float):
        fmt = "{:" + str(width) + ".3g}"
        return fmt.format(v)
    else:
        return "".join([" "] * (width - len(str(v))) + [str(v)])


event_loggers = {}


def lazy_setdefault(d, key, factory_fn):
    if key not in d:
        d[key] = factory_fn(key)
    return d[key]


def log_event(event, run=None, params=None):
    el = lazy_setdefault(event_loggers, run, EventLogger)
    el.log_event(event, params=params)


def add_update_callback(cb, run=None):
    add_callback("log_update", cb, run)


def add_completion_callback(cb, run=None):
    add_callback("log_completion", cb, run)


def add_callback(method, cb, run=None):
    assert method in ("log_update", "log_completion", "log_header", "log_snapshot")
    el = lazy_setdefault(event_loggers, run, EventLogger)
    old_log_update = getattr(el, method)

    def new_log_update(data):
        old_log_update(data)
        cb(data)

    setattr(el, method, new_log_update)
