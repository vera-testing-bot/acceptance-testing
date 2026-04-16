def flatten(lst):
    """Flatten a one-level-deep nested list."""
    result = []
    for sublist in lst:
        result.extend(sublist)
    return result


def is_sorted(lst):
    """Return True if lst is sorted in non-decreasing order."""
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    return True


def rotate_list(lst, k):
    """Rotate lst to the right by k positions."""
    if not lst:
        return []
    k = k % len(lst)
    return lst[-k:] + lst[:-k] if k else list(lst)


def zip_lists(a, b):
    """Return list of (a[i], b[i]) pairs, stopping at the shorter list."""
    return [(a[i], b[i]) for i in range(min(len(a), len(b)))]
