from src.math_utils import add, gcd


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 5) == 5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_gcd_basic():
    assert gcd(12, 8) == 4


def test_gcd_coprime():
    assert gcd(7, 13) == 1


def test_gcd_one_zero():
    assert gcd(0, 5) == 5
    assert gcd(5, 0) == 5


def test_gcd_same_number():
    assert gcd(6, 6) == 6


def test_gcd_negative_numbers():
    assert gcd(-12, 8) == 4
    assert gcd(12, -8) == 4
