import pytest

from src.prime_utils import is_prime


def test_numbers_less_than_two_are_not_prime():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(-5) is False


def test_two_is_prime():
    assert is_prime(2) is True


def test_small_primes():
    assert is_prime(3) is True
    assert is_prime(5) is True
    assert is_prime(7) is True
    assert is_prime(11) is True
    assert is_prime(13) is True


def test_small_composites():
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(9) is False
    assert is_prime(15) is False


def test_larger_prime():
    assert is_prime(97) is True


def test_larger_composite():
    assert is_prime(100) is False
