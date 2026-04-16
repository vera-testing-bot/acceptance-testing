from src.power_utils import power


def test_power_positive():
    assert power(2, 3) == 8


def test_power_zero_exponent():
    assert power(5, 0) == 1


def test_power_one_exponent():
    assert power(7, 1) == 7


def test_power_negative_exponent():
    assert power(2, -1) == 0.5


def test_power_zero_base():
    assert power(0, 5) == 0


def test_power_float_base():
    assert power(1.5, 2) == 2.25


def test_power_float_exponent():
    assert power(4, 0.5) == 2.0


def test_power_negative_base_even_exp():
    assert power(-3, 2) == 9


def test_power_negative_base_odd_exp():
    assert power(-2, 3) == -8
