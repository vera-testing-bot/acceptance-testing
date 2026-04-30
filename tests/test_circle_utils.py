import math

from src.circle_utils import area_of_circle


def test_area_of_circle_positive_radius():
    assert area_of_circle(2) == math.pi * 4


def test_area_of_circle_zero_radius():
    assert area_of_circle(0) == 0


def test_area_of_circle_float_radius():
    assert area_of_circle(1.5) == math.pi * 2.25
