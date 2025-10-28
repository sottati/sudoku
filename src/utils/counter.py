_count = 0

def increment():
    global _count
    _count += 1

def get_count():
    return _count

def reset():
    global _count
    _count = 0
