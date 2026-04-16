def to_binary(n: int) -> str:
    """Convert a non-negative integer to its binary string representation.

    The result has no '0b' prefix.
    """
    if n < 0:
        raise ValueError("to_binary requires a non-negative integer")
    if n == 0:
        return "0"
    bits = []
    while n:
        bits.append(str(n % 2))
        n //= 2
    return "".join(reversed(bits))


def from_binary(s: str) -> int:
    """Convert a binary string to an integer.

    Raises ValueError for invalid input.
    """
    if not s or not all(c in "01" for c in s):
        raise ValueError(f"invalid binary string: {s!r}")
    return int(s, 2)
