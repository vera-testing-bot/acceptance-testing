def chunk_list(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def deduplicate(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
