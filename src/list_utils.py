def find_duplicates(lst):
    seen = set()
    duplicates = []
    added = set()
    for item in lst:
        if item in seen and item not in added:
            duplicates.append(item)
            added.add(item)
        seen.add(item)
    return duplicates
