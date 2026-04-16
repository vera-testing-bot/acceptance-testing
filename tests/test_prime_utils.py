from src.prime_utils import is_prime


def test_zero_is_not_prime():
    assert is_prime(0) is False


def test_one_is_not_prime():
    assert is_prime(1) is False


def test_two_is_prime():
    assert is_prime(2) is True


def test_negative_numbers_are_not_prime():
    assert is_prime(-1) is False
    assert is_prime(-7) is False
    assert is_prime(-13) is False


def test_small_primes():
    for p in (3, 5, 7, 11, 13, 17, 19, 23):
        assert is_prime(p) is True


def test_small_composites():
    for c in (4, 6, 8, 9, 10, 12, 14, 15):
        assert is_prime(c) is False


def test_large_prime():
    assert is_prime(104729) is True


def test_large_composite():
    assert is_prime(104730) is False
