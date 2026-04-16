import pytest

from src.temp_utils import celsius_to_fahrenheit


def test_freezing_point():
    assert celsius_to_fahrenheit(0) == 32.0


def test_boiling_point():
    assert celsius_to_fahrenheit(100) == 212.0


def test_body_temperature():
    assert celsius_to_fahrenheit(37) == pytest.approx(98.6, abs=0.1)


def test_negative_celsius():
    assert celsius_to_fahrenheit(-40) == -40.0
