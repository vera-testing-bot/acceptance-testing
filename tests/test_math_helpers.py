from src.math_helpers import is_prime


def test_is_prime_less_than_one():
    assert is_prime(0) is False
    assert is_prime(-5) is False


def test_is_prime_one():
    assert is_prime(1) is False


def test_is_prime_two():
    assert is_prime(2) is True


def test_is_prime_small_primes():
    assert is_prime(3) is True
    assert is_prime(5) is True
    assert is_prime(7) is True


def test_is_prime_composite():
    assert is_prime(4) is False
    assert is_prime(9) is False
    assert is_prime(15) is False


def test_is_prime_larger_prime():
    assert is_prime(97) is True


def test_is_prime_larger_composite():
    assert is_prime(100) is False
