def to_roman(n: int) -> str:
    """Convert a positive integer (1–3999) to its Roman numeral representation."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError(f"Input must be an integer, got {type(n).__name__}")
    if n < 1 or n > 3999:
        raise ValueError(f"Input must be between 1 and 3999, got {n}")

    values = [
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

    result = []
    for value, numeral in values:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)
