import pytest

from src.bowling_ball import calculate_drop_time


def test_calculate_drop_time_zero_height():
    assert calculate_drop_time(0) == 0.0


def test_calculate_drop_time_returns_seconds():
    assert calculate_drop_time(19.62) == pytest.approx(2.0)


def test_calculate_drop_time_negative_height_raises():
    with pytest.raises(ValueError):
        calculate_drop_time(-1)
