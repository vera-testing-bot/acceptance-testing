from src.rand import random_point_in_sphere


def test_random_point_in_sphere_returns_n_coordinates():
    point = random_point_in_sphere(4)
    assert len(point) == 4


def test_random_point_in_sphere_coordinates_within_cube_bounds():
    point = random_point_in_sphere(6)
    assert all(-1.0 <= coordinate <= 1.0 for coordinate in point)


def test_random_point_in_sphere_lies_inside_unit_sphere():
    point = random_point_in_sphere(5)
    radius_squared = sum(coordinate * coordinate for coordinate in point)
    assert radius_squared <= 1.0


def test_random_point_in_sphere_rejects_non_positive_dimensions():
    try:
        random_point_in_sphere(0)
        assert False, "Expected ValueError for non-positive dimensions"
    except ValueError as exc:
        assert str(exc) == "n must be greater than 0"
