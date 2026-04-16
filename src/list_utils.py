def find_duplicates(lst: list) -> list:
    """Return a list of elements that appear more than once, in order of first duplicate occurrence.

    Each duplicate element appears only once in the result.
    """
    seen = set()
    duplicates = []
    duplicate_set = set()
    for item in lst:
        if item in seen and item not in duplicate_set:
            duplicates.append(item)
            duplicate_set.add(item)
        seen.add(item)
    return duplicates
