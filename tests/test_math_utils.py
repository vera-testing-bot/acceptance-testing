from src.math_utils import add, gcd


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 5) == 5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_gcd_common_divisor():
    assert gcd(12, 8) == 4


def test_gcd_second_zero():
    assert gcd(7, 0) == 7


def test_gcd_first_zero():
    assert gcd(0, 5) == 5


def test_gcd_coprimes():
    assert gcd(17, 13) == 1
