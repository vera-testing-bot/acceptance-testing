import math


def add(a, b):
    return a + b


def lcm(a: int, b: int) -> int:
    """Return the least common multiple of two positive integers."""
    return abs(a * b) // math.gcd(a, b)


def is_power_of_two(n: int) -> bool:
    """Return True if n is a power of two, False otherwise."""
    return n > 0 and (n & (n - 1)) == 0
