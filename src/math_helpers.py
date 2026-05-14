SPEED_OF_LIGHT_M_PER_S = 299_792_458
SPEED_OF_LIGHT_KM_PER_S = SPEED_OF_LIGHT_M_PER_S / 1_000
SPEED_OF_LIGHT_MI_PER_S = SPEED_OF_LIGHT_M_PER_S / 1_609.344

SPEED_OF_LIGHT = {
    "m/s": SPEED_OF_LIGHT_M_PER_S,
    "km/s": SPEED_OF_LIGHT_KM_PER_S,
    "mi/s": SPEED_OF_LIGHT_MI_PER_S,
}


def speed_of_light(unit: str = "m/s") -> float:
    """Return the speed of light for a supported unit."""
    if unit not in SPEED_OF_LIGHT:
        raise ValueError("Unsupported unit. Use one of: m/s, km/s, mi/s")
    return SPEED_OF_LIGHT[unit]


def multiply(a: int | float, b: int | float) -> int | float:
    """Return the product of a and b."""
    return a * b


def divide(a: int | float, b: int | float) -> float:
    """Return the result of a divided by b.

    Raises ValueError if b is 0.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def factorial(n: int) -> int:
    """Return n! (n factorial).

    Raises ValueError if n is negative.
    """
    if n < 0:
        raise ValueError("Cannot compute factorial of a negative number.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
