import os
import openai
import json
import itertools

def cached_events_iter(run_id, offset=0):
    '''
    Listing the events using the events endpoint may take a while, especially for
    longer runs with large batches.
    This function saves the events that have already been read
    into a local cache.
    '''
    events_it = None
    for line in itertools.count(start=offset):
        cache_filename = _get_cache_filename(run_id, line)
        if not events_it:
            try:
                with open(cache_filename) as f:
                    yield json.load(f)
                    continue
            except (OSError, json.decoder.JSONDecodeError):
                pass
        # TODO do a prefetch in a separate thread
        events_it = events_it or openai.Event.list(run=run_id, stream=True, offset=line, limit=1)
        try:
            event = next(events_it)
        except StopIteration:
            return
        with open(cache_filename, 'w') as f:
            json.dump(event, f)
        yield event

def _get_cache_filename(run_id, line):
    path = os.path.expanduser(f'~/.openai_finetune/events/{run_id}.{line}.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path
