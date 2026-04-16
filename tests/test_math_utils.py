from src.math_utils import add, clamp


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 5) == 5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_clamp_within_range():
    assert clamp(5, 1, 10) == 5


def test_clamp_below_min():
    assert clamp(0, 1, 10) == 1


def test_clamp_above_max():
    assert clamp(15, 1, 10) == 10


def test_clamp_at_min_boundary():
    assert clamp(1, 1, 10) == 1


def test_clamp_at_max_boundary():
    assert clamp(10, 1, 10) == 10
