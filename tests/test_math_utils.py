from src.math_utils import add, is_even


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 5) == 5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_is_even_even_number():
    assert is_even(4) is True


def test_is_even_odd_number():
    assert is_even(7) is False


def test_is_even_zero():
    assert is_even(0) is True


def test_is_even_negative_even():
    assert is_even(-2) is True


def test_is_even_negative_odd():
    assert is_even(-3) is False
