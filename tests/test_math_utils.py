from src.math_utils import add, gcd, is_even, lcm


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
    assert gcd(7, 5) == 1


def test_gcd_zero():
    assert gcd(0, 5) == 5


def test_gcd_same():
    assert gcd(6, 6) == 6


def test_lcm_basic():
    assert lcm(4, 6) == 12


def test_lcm_coprime():
    assert lcm(3, 5) == 15


def test_lcm_zero():
    assert lcm(0, 5) == 0


def test_is_even_even():
    assert is_even(4) is True


def test_is_even_odd():
    assert is_even(7) is False


def test_is_even_zero():
    assert is_even(0) is True
