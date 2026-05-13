import math

STANDARD_GRAVITY_METERS_PER_SECOND_SQUARED = 9.81


def calculate_drop_time(height: int | float) -> float:
    if height < 0:
        raise ValueError("Height must be non-negative.")

    return math.sqrt((2 * height) / STANDARD_GRAVITY_METERS_PER_SECOND_SQUARED)
