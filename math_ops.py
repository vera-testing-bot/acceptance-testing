import math


def multiply(a, b):
    return a * b


def power(base, exp):
    """
    Calculate the exponent of a number.
    
    Args:
        base: The base number
        exp: The exponent
    
    Returns:
        base raised to the power of exp
    
    Raises:
        ValueError: If base is 0 and exp is negative
    """
    if base == 0 and exp < 0:
        raise ValueError("Cannot raise 0 to a negative power")
    return base ** exp


def divide(a, b):
    """
    Divide one number by another with safe zero-division handling.

    Args:
        a: The dividend (numerator)
        b: The divisor (denominator)

    Returns:
        a / b for non-zero b

    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def absolute(n):
    """Return the absolute value of n."""
    if n < 0:
        return -n
    return n


def calculate_e():
    """
    Calculate Euler's number (e) to 6 decimal digits without using math functions.

    Uses the Taylor series expansion:
    e = 1 + 1/1! + 1/2! + 1/3! + ...

    Returns:
        An approximation of e accurate to 6 decimal places.
    """
    e = 1.0
    factorial = 1.0
    n = 1
    while True:
        factorial *= n
        term = 1.0 / factorial
        if term < 1e-7:
            break
        e += term
        n += 1
    return e


def pentagon_area(side_length):
    """Calculate the area of a regular pentagon from its side length."""
    if side_length <= 0:
        raise ValueError("Side length must be greater than zero")

    factor = math.sqrt(5 * (5 + 2 * math.sqrt(5)))
    return (side_length ** 2 * factor) / 4
