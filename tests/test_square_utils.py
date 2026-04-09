from src.square_utils import square


def test_square_positive():
    assert square(3) == 9


def test_square_negative():
    assert square(-2) == 4


def test_square_zero():
    assert square(0) == 0


def test_square_float():
    assert square(1.5) == 2.25
