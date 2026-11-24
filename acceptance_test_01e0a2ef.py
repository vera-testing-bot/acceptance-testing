"""Validation helper for acceptance-test run 01e0a2ef."""


def validate_bounds(value: float, min_value: float, max_value: float) -> int | float:
    """Return ``value`` if it lies within the inclusive bounds.

    Raises:
        ValueError: If ``value`` is less than ``min_value`` or greater than
        ``max_value``.
    """
    if value < min_value or value > max_value:
        raise ValueError(
            f"value {value} is outside the allowed range [{min_value}, {max_value}]"
        )
    return value
