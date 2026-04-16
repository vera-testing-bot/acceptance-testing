def sum_list(lst):
    """Return the sum of all elements in the list. Returns 0 for empty list."""
    return sum(lst)


def product_list(lst):
    """Return the product of all elements in the list. Returns 1 for empty list."""
    result = 1
    for item in lst:
        result *= item
    return result


def flatten(lst):
    """Flatten a nested list one level deep."""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result


def is_sorted(lst):
    """Return True if the list is sorted in non-decreasing order."""
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    return True


def chunk_list(lst, size):
    """Split a list into chunks of the given size."""
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def deduplicate(lst):
    """Return a new list with duplicates removed, preserving order."""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def zip_lists(lst1, lst2):
    """Zip two lists into a list of pairs, truncating to the shorter length."""
    return list(zip(lst1, lst2))


def sliding_window(lst, size):
    """Return a list of all sliding windows of the given size."""
    if size > len(lst):
        return []
    return [lst[i:i + size] for i in range(len(lst) - size + 1)]
