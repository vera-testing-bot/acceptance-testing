import math


OVERLAP_BAND_WIDTH_INCHES = 0.08
PEPPERONI_THICKNESS_INCHES = 0.1
PEPPERONI_DENSITY_LB_PER_CUBIC_INCH = 0.038


def add(a, b):
    return a + b


def clamp(value, min_value, max_value):
    """Constrains a value to the inclusive range [min_value, max_value]."""
    return max(min_value, min(value, max_value))


def multiply(a, b):
    return a * b


def negate(n):
    return -n


def is_even(n):
    """Returns True when n is divisible by 2."""
    return n % 2 == 0


def is_perfect_number(n):
    if n <= 1:
        return False

    divisor_sum = 1
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            divisor_sum += candidate
            pair = n // candidate
            if pair != candidate:
                divisor_sum += pair
        candidate += 1

    return divisor_sum == n


def is_kaprekar_number(n):
    if n < 0:
        return False
    if n == 1:
        return True

    square = n * n
    square_text = str(square)

    for split_index in range(1, len(square_text)):
        left_part = int(square_text[:split_index])
        right_part = int(square_text[split_index:])
        if right_part == 0:
            continue
        if add(left_part, right_part) == n:
            return True

    return False


def calculate_pepperoni_lbs(pizza_diameter, pepperoni_diameter):
    if pizza_diameter <= 0 or pepperoni_diameter <= 0:
        raise ValueError("diameters must be positive")

    pepperoni_radius = pepperoni_diameter / 2
    pizza_radius = pizza_diameter / 2

    pizza_area = math.pi * pizza_radius * pizza_radius
    pepperoni_area = math.pi * pepperoni_radius * pepperoni_radius

    effective_coverage_radius = max(pepperoni_radius - OVERLAP_BAND_WIDTH_INCHES, 0.01)
    effective_coverage_area = (
        math.pi * effective_coverage_radius * effective_coverage_radius
    )

    slices_needed = pizza_area / effective_coverage_area
    pounds_per_slice = (
        pepperoni_area
        * PEPPERONI_THICKNESS_INCHES
        * PEPPERONI_DENSITY_LB_PER_CUBIC_INCH
    )

    return slices_needed * pounds_per_slice


def hello_spec_audit_1778114263():
    return 42


def hello_spec_audit():
    return 42
