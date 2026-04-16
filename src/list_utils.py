def remove_duplicates(lst: list) -> list:
    """Return a new list with duplicates removed, preserving order."""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
