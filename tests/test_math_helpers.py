import pytest

from src.math_helpers import calculate_sphere_volume, divide, factorial, multiply


def test_multiply_positive():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(5, 0) == 0


def test_multiply_negative():
    assert multiply(-2, 3) == -6


def test_multiply_floats():
    assert multiply(2.5, 4) == 10.0


def test_divide_basic():
    assert divide(10, 2) == 5.0


def test_divide_negative():
    assert divide(-9, 3) == -3.0


def test_divide_floats():
    assert divide(7.5, 2.5) == 3.0


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(5, 0)


def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_one():
    assert factorial(1) == 1


def test_factorial_positive():
    assert factorial(5) == 120


def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-1)


def test_calculate_sphere_volume_zero_radius():
    assert calculate_sphere_volume(0) == 0.0


def test_calculate_sphere_volume_positive_radius():
    assert calculate_sphere_volume(3) == pytest.approx(113.09733552923255)


def test_calculate_sphere_volume_negative_radius():
    with pytest.raises(ValueError):
        calculate_sphere_volume(-1)
