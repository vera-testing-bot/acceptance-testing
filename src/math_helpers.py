import math


STANDARD_GRAVITY_METERS_PER_SECOND_SQUARED = 9.81


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


def calculate_drop_time(height: int | float) -> float:
    """Return drop time in seconds for a given height in meters."""
    if height < 0:
        raise ValueError("Height must be non-negative.")

    return math.sqrt((2 * height) / STANDARD_GRAVITY_METERS_PER_SECOND_SQUARED)
