import pytest

from src.math_helpers import divide, factorial, multiply, spring_force


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


def test_spring_force_at_rest_length():
    assert spring_force(10, 2, 2) == 0


def test_spring_force_stretched():
    assert spring_force(5, 1, 3) == -10


def test_spring_force_compressed():
    assert spring_force(8, 4, 2.5) == 12.0


def test_spring_force_zero_constant():
    assert spring_force(0, 3, 8) == 0


def test_spring_force_negative_constant():
    with pytest.raises(ValueError):
        spring_force(-1, 2, 3)
