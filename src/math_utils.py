def add(a, b):
    return a + b


def negate(n):
    return -n


def is_even(n):
    return n % 2 == 0


def is_perfect_number(n):
    if n <= 1:
        return False

    divisor_sum = 1
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            divisor_sum += candidate
            pair = n // candidate
            if pair != candidate:
                divisor_sum += pair
        candidate += 1

    return divisor_sum == n
