import pytest

import math

from src.math_helpers import (
    SPEED_OF_LIGHT,
    SPEED_OF_LIGHT_KM_PER_S,
    SPEED_OF_LIGHT_M_PER_S,
    SPEED_OF_LIGHT_MI_PER_S,
    divide,
    factorial,
    multiply,
    speed_of_light,
)


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


def test_speed_of_light_constants_in_multiple_units():
    assert SPEED_OF_LIGHT_M_PER_S == 299_792_458
    assert SPEED_OF_LIGHT_KM_PER_S == 299_792.458
    assert math.isclose(SPEED_OF_LIGHT_MI_PER_S, 186_282.39705122002)


def test_speed_of_light_mapping():
    assert SPEED_OF_LIGHT["m/s"] == SPEED_OF_LIGHT_M_PER_S
    assert SPEED_OF_LIGHT["km/s"] == SPEED_OF_LIGHT_KM_PER_S
    assert SPEED_OF_LIGHT["mi/s"] == SPEED_OF_LIGHT_MI_PER_S


def test_speed_of_light_returns_value_for_unit():
    assert speed_of_light("m/s") == SPEED_OF_LIGHT_M_PER_S
    assert speed_of_light("km/s") == SPEED_OF_LIGHT_KM_PER_S
    assert speed_of_light("mi/s") == SPEED_OF_LIGHT_MI_PER_S


def test_speed_of_light_rejects_unsupported_unit():
    with pytest.raises(ValueError, match="Unsupported unit"):
        speed_of_light("ft/s")
