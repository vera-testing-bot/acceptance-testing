def add(a, b):
    return a + b


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of a and b."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Return the least common multiple of a and b."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def is_even(n: int) -> bool:
    """Return True if n is even, False otherwise."""
    return n % 2 == 0
