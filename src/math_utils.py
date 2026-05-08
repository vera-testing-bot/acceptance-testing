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


def is_kaprekar_number(n):
    if n < 0:
        return False
    if n == 1:
        return True

    square = n * n
    square_text = str(square)

    for split_index in range(1, len(square_text)):
        left_part = int(square_text[:split_index])
        right_part = int(square_text[split_index:])
        if right_part == 0:
            continue
        if add(left_part, right_part) == n:
            return True

    return False


def hello_spec_audit_1778114263():
    return 42


def hello_spec_audit():
    return 42
