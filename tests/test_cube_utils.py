from src.cube_utils import cube, cube_surface_area


def test_cube_positive():
    assert cube(2) == 8


def test_cube_negative():
    assert cube(-3) == -27


def test_cube_zero():
    assert cube(0) == 0


def test_cube_float():
    assert cube(1.5) == 3.375


def test_cube_surface_area():
    assert cube_surface_area(2) == 24
