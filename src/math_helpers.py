def multiply(a: int | float, b: int | float) -> int | float:
    """Return the product of a and b."""
    return a * b


def divide(a: int | float, b: int | float) -> float:
    """Return the result of a divided by b.

    Raises ValueError if b is 0.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def factorial(n: int) -> int:
    """Return n! (n factorial).

    Raises ValueError if n is negative.
    """
    if n < 0:
        raise ValueError("Cannot compute factorial of a negative number.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def quantile(values: list[int | float], q: float) -> float:
    """Return the q-th quantile for a list of numeric values.

    Uses linear interpolation between adjacent ranks.
    Raises ValueError if values is empty or q is outside [0, 1].
    """
    if not values:
        raise ValueError("Cannot compute quantile of an empty list.")
    if q < 0 or q > 1:
        raise ValueError("Quantile must be between 0 and 1.")

    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])

    position = q * (len(ordered) - 1)
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(ordered) - 1)
    fraction = position - lower_index

    lower = ordered[lower_index]
    upper = ordered[upper_index]
    return float(lower + (upper - lower) * fraction)
