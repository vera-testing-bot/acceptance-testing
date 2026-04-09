from src.math_helpers import is_even


def test_is_even_even_number():
    assert is_even(4) is True


def test_is_even_odd_number():
    assert is_even(3) is False


def test_is_even_zero():
    assert is_even(0) is True


def test_is_even_negative_even():
    assert is_even(-2) is True


def test_is_even_negative_odd():
    assert is_even(-1) is False
