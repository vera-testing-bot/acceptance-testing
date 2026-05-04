import pytest

from src.math_helpers import area_of_regular_septigon, divide, factorial, multiply


def test_multiply_positive():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(5, 0) == 0


def test_multiply_negative():
    assert multiply(-2, 3) == -6


def test_multiply_floats():
    assert multiply(2.5, 4) == 10.0


def test_divide_basic():
    assert divide(10, 2) == 5.0


def test_divide_negative():
    assert divide(-9, 3) == -3.0


def test_divide_floats():
    assert divide(7.5, 2.5) == 3.0


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(5, 0)


def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_one():
    assert factorial(1) == 1


def test_factorial_positive():
    assert factorial(5) == 120


def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-1)


def test_area_of_regular_septigon_unit_side():
    assert area_of_regular_septigon(1) == pytest.approx(3.633912444001589)


def test_area_of_regular_septigon_scales_with_square_of_side():
    assert area_of_regular_septigon(2) == pytest.approx(14.535649776006356)


@pytest.mark.parametrize("side_length", [0, -1, -2.5])
def test_area_of_regular_septigon_rejects_non_positive_side_length(side_length):
    with pytest.raises(ValueError, match="Side length must be positive"):
        area_of_regular_septigon(side_length)
