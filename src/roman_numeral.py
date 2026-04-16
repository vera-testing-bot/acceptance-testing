_ROMAN_VALUES = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]


def to_roman(n: int) -> str:
    """Convert a positive integer (1–3999) to its Roman numeral representation.

    Raises ValueError for out-of-range inputs.
    """
    if not (1 <= n <= 3999):
        raise ValueError(f"to_roman requires an integer between 1 and 3999, got {n}")
    result = []
    for value, numeral in _ROMAN_VALUES:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)
