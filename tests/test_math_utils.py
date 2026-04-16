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
    assert lcm(5, 7) == 35


def test_lcm_same_number():
    assert lcm(8, 8) == 8


def test_lcm_one():
    assert lcm(1, 9) == 9


def test_lcm_zero():
    assert lcm(0, 5) == 0


def test_lcm_negative():
    assert lcm(-4, 6) == 12
