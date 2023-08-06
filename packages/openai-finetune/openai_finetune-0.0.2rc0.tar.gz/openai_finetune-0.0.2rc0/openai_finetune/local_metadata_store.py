import os
import os.path as osp
import json


_store_dir = osp.join(osp.expanduser("~"), ".openai_finetune", "meta")
os.makedirs(_store_dir, exist_ok=True)


def save(plan, data):
    with open(_make_path(plan), "w") as f:
        json.dump(data, f)


def load(plan):
    try:
        with open(_make_path(plan), "r") as f:
            return json.load(f)
    except OSError:
        return {}


def _make_path(plan):
    path = osp.join(_store_dir, plan + ".json")
    return path
