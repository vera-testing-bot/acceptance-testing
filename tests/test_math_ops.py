from math_ops import multiply, power, divide
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
    assert power(2, -1) == 0.5


def test_power_zero_base_negative_exponent():
    with pytest.raises(ValueError, match="Cannot raise 0 to a negative power"):
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
