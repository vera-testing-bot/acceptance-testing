def is_sorted(lst: list) -> bool:
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))
