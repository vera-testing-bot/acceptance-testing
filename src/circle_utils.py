import math


def area_of_circle(radius: int | float) -> float:
    if radius < 0:
        raise ValueError("radius must be non-negative")
    return math.pi * radius * radius
