import pytest
from src.math_utils import add, is_prime, factorial


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 5) == 5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_is_prime_two():
    assert is_prime(2) is True


def test_is_prime_three():
    assert is_prime(3) is True


def test_is_prime_four():
    assert is_prime(4) is False


def test_is_prime_one():
    assert is_prime(1) is False


def test_is_prime_zero():
    assert is_prime(0) is False


def test_is_prime_thirteen():
    assert is_prime(13) is True


def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_one():
    assert factorial(1) == 1


def test_factorial_five():
    assert factorial(5) == 120


def test_factorial_ten():
    assert factorial(10) == 3628800


def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        factorial(-1)
