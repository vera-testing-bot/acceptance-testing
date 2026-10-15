import pytest

from acceptance_test_01e0a2ef import validate_bounds


def test_validate_bounds_accepts_in_range_value():
    assert validate_bounds(5, 1, 10) == 5


def test_validate_bounds_rejects_below_minimum():
    with pytest.raises(ValueError):
        validate_bounds(0, 1, 10)


def test_validate_bounds_rejects_above_maximum():
    with pytest.raises(ValueError):
        validate_bounds(11, 1, 10)
