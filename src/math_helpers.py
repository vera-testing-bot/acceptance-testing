SPEED_OF_LIGHT_M_PER_S = 299_792_458
SPEED_OF_LIGHT_KM_PER_S = SPEED_OF_LIGHT_M_PER_S / 1_000
SPEED_OF_LIGHT_MI_PER_S = SPEED_OF_LIGHT_M_PER_S / 1_609.344

EARTH_GRAVITY_M_PER_S2 = 9.80665
GRAVITATIONAL_CONSTANT_M3_PER_KG_S2 = 6.67430e-11
PLANCK_CONSTANT_J_S = 6.62607015e-34
AVOGADRO_CONSTANT_PER_MOL = 6.02214076e23

SPEED_OF_LIGHT = {
    "m/s": SPEED_OF_LIGHT_M_PER_S,
    "km/s": SPEED_OF_LIGHT_KM_PER_S,
    "mi/s": SPEED_OF_LIGHT_MI_PER_S,
}

PHYSICS_CONSTANTS = {
    "gravity": EARTH_GRAVITY_M_PER_S2,
    "gravitational_constant": GRAVITATIONAL_CONSTANT_M3_PER_KG_S2,
    "planck_constant": PLANCK_CONSTANT_J_S,
    "avogadro_constant": AVOGADRO_CONSTANT_PER_MOL,
}


def speed_of_light(unit: str = "m/s") -> float:
    """Return the speed of light for a supported unit."""
    if unit not in SPEED_OF_LIGHT:
        raise ValueError("Unsupported unit. Use one of: m/s, km/s, mi/s")
    return SPEED_OF_LIGHT[unit]


def physics_constant(name: str) -> float:
    """Return a supported physics constant by name."""
    if name not in PHYSICS_CONSTANTS:
        raise ValueError(
            "Unsupported constant. Use one of: gravity, gravitational_constant, "
            "planck_constant, avogadro_constant"
        )
    return PHYSICS_CONSTANTS[name]


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
