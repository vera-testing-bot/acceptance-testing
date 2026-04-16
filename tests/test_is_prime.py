from is_prime import is_prime


def test_negative_numbers_not_prime():
    assert is_prime(-1) is False
    assert is_prime(-7) is False


def test_zero_not_prime():
    assert is_prime(0) is False


def test_one_not_prime():
    assert is_prime(1) is False


def test_two_is_prime():
    assert is_prime(2) is True


def test_three_is_prime():
    assert is_prime(3) is True


def test_even_numbers_not_prime():
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(100) is False


def test_small_primes():
    for p in [5, 7, 11, 13, 17, 19, 23]:
        assert is_prime(p) is True


def test_composite_numbers():
    for c in [9, 15, 21, 25, 49]:
        assert is_prime(c) is False


def test_large_prime():
    assert is_prime(97) is True


def test_large_composite():
    assert is_prime(91) is False  # 7 * 13
