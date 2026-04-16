from src.list_utils import sum_list


def test_sum_list_empty():
    assert sum_list([]) == 0


def test_sum_list_positive():
    assert sum_list([1, 2, 3]) == 6


def test_sum_list_negative():
    assert sum_list([-1, -2, -3]) == -6


def test_sum_list_mixed():
    assert sum_list([1, -1, 2, -2]) == 0


def test_sum_list_single():
    assert sum_list([5]) == 5


def test_sum_list_floats():
    assert sum_list([1.5, 2.5]) == 4.0
