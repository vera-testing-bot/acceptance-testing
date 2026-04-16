def sliding_window(lst, size):
    if size <= 0 or size > len(lst):
        return []
    return [lst[i:i + size] for i in range(len(lst) - size + 1)]
