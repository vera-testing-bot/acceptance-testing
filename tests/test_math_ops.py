from math_ops import (
    absolute,
    calculate_e,
    calculate_p_2_pairs,
    divide,
    multiply,
    power,
    sin,
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


# Power function tests
def test_power_positive():
    assert power(2, 3) == 8


def test_power_zero_exponent():
    assert power(2, 0) == 1


def test_power_zero_base_zero_exponent():
    assert power(0, 0) == 1


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
def test_absolute_positive():
    assert absolute(7) == 7


def test_absolute_negative():
    assert absolute(-7) == 7


def test_absolute_zero():
    assert absolute(0) == 0


# Calculate e tests
def test_calculate_e_accuracy():
    # e to 6 decimal places is 2.718282
    result = calculate_e()
    assert round(result, 6) == 2.718282


def test_calculate_e_no_math_module():
    # Ensure the function works without importing math
    import math_ops
    assert hasattr(math_ops, 'calculate_e')
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
