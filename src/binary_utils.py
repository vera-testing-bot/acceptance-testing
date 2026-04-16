def to_binary(n: int) -> str:
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    return bin(n)[2:]


def from_binary(s: str) -> int:
    if not s or not all(c in "01" for c in s):
        raise ValueError(f"Invalid binary string: {s!r}")
    return int(s, 2)
