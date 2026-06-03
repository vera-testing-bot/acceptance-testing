import math

import pytest

from src.circle_utils import area_of_circle


def test_area_of_circle_positive_radius():
    assert area_of_circle(2) == math.pi * 4


def test_area_of_circle_zero_radius():
    assert area_of_circle(0) == 0


def test_area_of_circle_float_radius():
    assert area_of_circle(1.5) == math.pi * 2.25


def test_area_of_circle_negative_radius_raises():
    with pytest.raises(ValueError, match="radius must be non-negative"):
        area_of_circle(-1)
