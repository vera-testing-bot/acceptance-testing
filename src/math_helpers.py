import math


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


def area_of_regular_septigon(side_length: int | float) -> float:
    """Return the area of a regular septigon for the given side length."""
    if side_length <= 0:
        raise ValueError("Side length must be positive")

    sides = 7
    return (sides * (side_length**2)) / (4 * math.tan(math.pi / sides))
