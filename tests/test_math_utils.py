from src.math_utils import add, lcm


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 5) == 5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_lcm_basic():
    assert lcm(4, 6) == 12


def test_lcm_coprime():
    assert lcm(3, 5) == 15


def test_lcm_same_number():
    assert lcm(7, 7) == 7


def test_lcm_one():
    assert lcm(1, 9) == 9
