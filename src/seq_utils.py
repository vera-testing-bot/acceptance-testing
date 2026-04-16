def nth_fibonacci(n):
    """Return the nth Fibonacci number (0-indexed: F(0)=0, F(1)=1, F(2)=1, ...)."""
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
