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


def spring_force(
    spring_constant: int | float,
    rest_length: int | float,
    current_length: int | float,
) -> int | float:
    """Return spring force using Hooke's law.

    Force is positive when compressed and negative when stretched.

    Raises ValueError if spring_constant is negative.
    """
    if spring_constant < 0:
        raise ValueError("Spring constant cannot be negative.")

    displacement = current_length - rest_length
    return -spring_constant * displacement
