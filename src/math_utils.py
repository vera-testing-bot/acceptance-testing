def add(a, b):
    return a + b


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of two non-negative integers using the Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a


def sum_digits(n: int) -> int:
    """Return the sum of the decimal digits of a non-negative integer."""
    return sum(int(d) for d in str(n))
