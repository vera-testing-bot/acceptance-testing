def add(a, b):
    return a + b


def negate(n):
    return -n


def is_even(n):
    return n % 2 == 0


def sin(x):
    pi = 3.141592653589793
    two_pi = 2.0 * pi

    x = x % two_pi
    if x > pi:
        x -= two_pi

    if x > (pi / 2):
        x = pi - x
    elif x < (-pi / 2):
        x = -pi - x

    term = x
    result = x
    n = 1
    while abs(term) > 1e-12 and n < 50:
        term *= -(x * x) / ((2 * n) * (2 * n + 1))
        result += term
        n += 1

    return result
