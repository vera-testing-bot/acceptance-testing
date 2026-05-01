import pytest

from src.hexagon_utils import regular_hexagon_area


def test_regular_hexagon_area_integer_side():
    assert regular_hexagon_area(2) == pytest.approx(10.392304845413264)


def test_regular_hexagon_area_float_side():
    assert regular_hexagon_area(1.5) == pytest.approx(5.845671475544961)


def test_regular_hexagon_area_zero_side():
    assert regular_hexagon_area(0) == 0.0
