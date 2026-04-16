def rotate_list(lst, k):
    """Return a new list rotated to the right by k positions."""
    if not lst:
        return []
    k = k % len(lst)
    return lst[-k:] + lst[:-k] if k else list(lst)


def group_by(lst, key_fn):
    """Group list elements into a dict keyed by key_fn(element)."""
    result = {}
    for item in lst:
        key = key_fn(item)
        result.setdefault(key, []).append(item)
    return result
