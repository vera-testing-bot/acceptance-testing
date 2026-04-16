import math


def add(a, b):
    return a + b


def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(abs(a), abs(b))
