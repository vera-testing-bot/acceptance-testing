import math
from math_ops import (
    absolute,
    calculate_e,
    calculate_p_2_pairs,
    divide,
    multiply,
    power,
    rectangle_area,
    sin,
    stddev,
    volume_of_sphere,
)
import pytest


def test_multiply_positive():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(5, 0) == 0


def test_multiply_negative():
    assert multiply(-2, 3) == -6


def test_multiply_floats():
    assert multiply(2.5, 4) == 10.0


def test_rectangle_area_positive():
    assert rectangle_area(5, 3) == 15


def test_rectangle_area_zero_side():
    assert rectangle_area(5, 0) == 0


def test_rectangle_area_floats():
    assert rectangle_area(2.5, 4.0) == 10.0


# Power function tests
@pytest.mark.spec("math-operations.arithmetic.power-integers")
def test_power_positive():
    assert power(2, 3) == 8


@pytest.mark.spec("math-operations.arithmetic.power-zero")
def test_power_zero_exponent():
    assert power(2, 0) == 1


@pytest.mark.spec("math-operations.arithmetic.power-has-tests")
def test_power_zero_base_zero_exponent():
    assert power(0, 0) == 1


@pytest.mark.spec("math-operations.arithmetic.power-negative-exp")
def test_power_negative_exponent():
    with pytest.raises(ValueError, match="Negative exponents are not supported"):
        power(2, -1)


def test_power_zero_base_negative_exponent():
    with pytest.raises(ValueError, match="Negative exponents are not supported"):
        power(0, -1)


# Divide function tests
def test_divide_positive():
    assert divide(10, 2) == 5


def test_divide_by_one():
    assert divide(5, 1) == 5


def test_divide_floats():
    assert divide(7.5, 2.5) == 3.0


def test_divide_negative():
    assert divide(-10, 2) == -5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)


def test_divide_by_zero_float_raises_with_consistent_message():
    with pytest.raises(ValueError, match=r"^Cannot divide by zero\.$"):
        divide(5, 0.0)


# Absolute value tests
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (7, 7),
        (-7, 7),
        (0, 0),
    ],
)
def test_absolute_returns_non_negative_magnitude(value, expected):
    assert absolute(value) == expected


def test_absolute_negative_zero_returns_positive_zero():
    result = absolute(-0.0)
    assert result == 0.0
    assert math.copysign(1.0, result) == 1.0


# Calculate e tests
def test_calculate_e_accuracy():
    # e to 6 decimal places is 2.718282
    result = calculate_e()
    assert round(result, 6) == 2.718282


def test_calculate_e_no_math_module():
    # Ensure the function works without importing math
    import math_ops

    assert hasattr(math_ops, "calculate_e")
    assert calculate_e() > 2.718280
    assert calculate_e() < 2.718282


# Sine function tests
def test_sin_zero():
    assert sin(0.0) == pytest.approx(0.0, abs=1e-6)


def test_sin_pi_over_two():
    pi = 3.141592653589793
    assert sin(pi / 2) == pytest.approx(1.0, abs=1e-6)


def test_sin_negative_pi_over_two():
    pi = 3.141592653589793
    assert sin(-pi / 2) == pytest.approx(-1.0, abs=1e-6)


def test_sin_pi_is_zero():
    pi = 3.141592653589793
    assert sin(pi) == pytest.approx(0.0, abs=1e-6)


def test_sin_periodicity_large_input():
    pi = 3.141592653589793
    assert sin(5 * pi / 2) == pytest.approx(1.0, abs=1e-6)


def test_calculate_p_2_pairs_returns_expected_probability():
    result = calculate_p_2_pairs()
    assert isinstance(result, float)
    assert result == pytest.approx(0.047539, abs=1e-6)


def test_volume_of_sphere_zero_radius():
    assert volume_of_sphere(0) == 0.0


def test_volume_of_sphere_positive_radius():
    assert volume_of_sphere(3) == pytest.approx(113.09733552923255)


def test_volume_of_sphere_negative_radius_raises():
    with pytest.raises(ValueError, match="Radius cannot be negative"):
        volume_of_sphere(-1)


@pytest.mark.spec("math-operations.statistics.stddev-basic")
def test_stddev_returns_population_standard_deviation_for_integers():
    numbers = [2, 4, 4, 4, 5, 5, 7, 9]
    assert stddev(numbers) == pytest.approx(2.0, abs=1e-9)


@pytest.mark.spec("math-operations.statistics.stddev-basic")
def test_stddev_returns_population_standard_deviation_for_floats():
    numbers = [1.5, 2.5, 3.5, 4.5]
    assert stddev(numbers) == pytest.approx(1.118033988749895, abs=1e-12)


@pytest.mark.spec("math-operations.statistics.stddev-single-value")
def test_calculate_stddev_single_value_is_zero():
    assert stddev([5]) == 0.0


@pytest.mark.spec("math-operations.statistics.stddev-empty-input")
def test_calculate_stddev_raises_for_empty_input():
    with pytest.raises(ValueError, match="numbers must not be empty"):
        stddev([])


@pytest.mark.spec("math-operations.statistics.stddev-no-statistics-module")
def test_calculate_stddev_without_statistics_module_dependency():
    result = stddev([1, 2, 3])
    assert result == pytest.approx(0.816496580927726, abs=1e-12)
