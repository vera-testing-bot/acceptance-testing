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


def calculate_sphere_volume(radius: int | float) -> float:
    """Return the volume of a sphere for the given radius.

    Raises ValueError if radius is negative.
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    return (4.0 / 3.0) * 3.141592653589793 * (radius ** 3)
