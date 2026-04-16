import pytest

from src.math_utils import add, average


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 5) == 5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_average_positive_numbers():
    assert average([1, 2, 3, 4, 5]) == 3.0


def test_average_negative_numbers():
    assert average([-1, -2, -3]) == -2.0


def test_average_single_element():
    assert average([7]) == 7.0


def test_average_floats():
    assert average([1.5, 2.5, 3.0]) == pytest.approx(2.333333, rel=1e-5)


def test_average_empty_list_raises():
    with pytest.raises(ValueError):
        average([])
