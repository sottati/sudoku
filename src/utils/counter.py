_counters = {}

def increment(counter_id='default'):
    global _counters
    if counter_id not in _counters:
        _counters[counter_id] = 0
    _counters[counter_id] += 1

def get_count(counter_id='default'):
    return _counters.get(counter_id, 0)

def reset(counter_id=None):
    global _counters
    if counter_id:
        _counters[counter_id] = 0
    else:
        _counters.clear()
