from src.math_utils import add, negate


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 5) == 5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_negate_positive():
    assert negate(5) == -5


def test_negate_negative():
    assert negate(-2) == 2


def test_negate_zero():
    assert negate(0) == 0
