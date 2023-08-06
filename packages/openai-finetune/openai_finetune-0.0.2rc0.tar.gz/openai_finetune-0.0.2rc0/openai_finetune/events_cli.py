import sys
import openai
import argparse
from .cli import configure_openai, add_openai_args
from .event_logger import log_event
from .local_events_cache import cached_events_iter


def add_events_args(parser):
    parser.add_argument("--run", "-r", required=True, help="Run id")
    # parser.add_argument('--no-stream', destination="stream", default=True, action="store_false", help="List the ")


def list_events(run, stream=False):
    assert stream
    events_it = cached_events_iter(run)
    # events_it = openai.Event.list(run=run, stream=stream, limit=1)
    if not stream:
        events_it = events_it["data"]
    for event in events_it:
        log_event(event["data"], run)


def main():
    parser = argparse.ArgumentParser(
        description="List the events for a batch-mode fine-tuning run"
    )
    add_events_args(parser)
    add_openai_args(parser)
    args = parser.parse_args()
    configure_openai(args)
    list_events(args.run, True)


if __name__ == "__main__":
    main()
