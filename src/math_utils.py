def add(a, b):
    return a + b


def average(lst):
    """Return the arithmetic mean of a list of numbers. Raises ValueError for empty list."""
    if not lst:
        raise ValueError("Cannot compute average of empty list")
    return sum(lst) / len(lst)


def clamp(value, min_val, max_val):
    """Clamp value to the range [min_val, max_val]."""
    return max(min_val, min(max_val, value))


def is_prime(n):
    """Return True if n is a prime number."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def factorial(n):
    """Return the factorial of a non-negative integer n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
