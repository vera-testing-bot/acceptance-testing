def add(a, b):
    return a + b


def clamp(value, min_val, max_val):
    """Return value clamped to [min_val, max_val]."""
    if value < min_val:
        return min_val
    if value > max_val:
        return max_val
    return value
