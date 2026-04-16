from src.math_utils import add, gcd, lcm


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


def test_gcd_same_numbers():
    assert gcd(6, 6) == 6


def test_gcd_with_zero():
    assert gcd(0, 5) == 5


def test_gcd_negative_inputs():
    assert gcd(-12, 8) == 4


def test_lcm_basic():
    assert lcm(4, 6) == 12


def test_lcm_coprime():
    assert lcm(3, 7) == 21


def test_lcm_same_numbers():
    assert lcm(5, 5) == 5


def test_lcm_with_zero():
    assert lcm(0, 7) == 0
