from src.triangle_utils import calculate_triangle_area


def test_calculate_triangle_area_with_positive_numbers():
    assert calculate_triangle_area(10, 5) == 25


def test_calculate_triangle_area_with_zero_base():
    assert calculate_triangle_area(0, 5) == 0


def test_calculate_triangle_area_with_float_values():
    assert calculate_triangle_area(3.5, 2.0) == 3.5
