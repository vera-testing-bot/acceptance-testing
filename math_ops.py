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
        ValueError: If exp is negative
    """
    if exp < 0:
        raise ValueError("Negative exponents are not supported")
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
        raise ValueError("Cannot divide by zero.")
    return a / b


def absolute(n):
    """Return the absolute value of n."""
    if n == 0:
        return n + 0
    return -n if n < 0 else n


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


def calculate_p_2_pairs():
    """Return the probability of exactly two pairs in a 5-card poker hand."""
    pair_rank_choices = 78
    pair_suit_choices = 36
    kicker_choices = 44
    two_pair_hands = pair_rank_choices * pair_suit_choices * kicker_choices
    total_hands = 2_598_960
    return two_pair_hands / total_hands


def sin(x):
    """Return sin(x) without using the math module."""
    pi = 3.141592653589793
    two_pi = 2 * pi

    # Reduce x to [-pi, pi] for faster convergence.
    x = x % two_pi
    if x > pi:
        x -= two_pi

    term = x
    result = x
    n = 1

    while True:
        term *= -x * x / ((2 * n) * (2 * n + 1))
        if abs(term) < 1e-15:
            break
        result += term
        n += 1

    return result
