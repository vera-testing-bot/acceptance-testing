from src.math_utils import add, sum_digits


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 5) == 5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_sum_digits_zero():
    assert sum_digits(0) == 0


def test_sum_digits_single():
    assert sum_digits(9) == 9


def test_sum_digits_multi():
    assert sum_digits(123) == 6


def test_sum_digits_large():
    assert sum_digits(9999) == 36
