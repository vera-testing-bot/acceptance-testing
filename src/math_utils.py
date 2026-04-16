def add(a, b):
    return a + b


def lcm(a, b):
    from math import gcd
    return a * b // gcd(a, b)
