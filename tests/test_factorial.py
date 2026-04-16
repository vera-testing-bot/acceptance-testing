import pytest
from src.factorial import factorial


def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_one():
    assert factorial(1) == 1


def test_factorial_small_positive():
    assert factorial(5) == 120


def test_factorial_another_positive():
    assert factorial(4) == 24


def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        factorial(-1)
