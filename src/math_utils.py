def add(a, b):
    return a + b


def average(lst: list[int | float]) -> float:
    """Return the arithmetic mean of a list of numbers.

    Raises ValueError if lst is empty.
    """
    if not lst:
        raise ValueError("Cannot compute average of an empty list.")
    return sum(lst) / len(lst)
