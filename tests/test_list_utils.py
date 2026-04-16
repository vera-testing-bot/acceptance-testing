from src.list_utils import sliding_window


def test_basic():
    assert sliding_window([1, 2, 3, 4], 2) == [[1, 2], [2, 3], [3, 4]]


def test_window_equals_length():
    assert sliding_window([1, 2, 3], 3) == [[1, 2, 3]]


def test_window_size_one():
    assert sliding_window([1, 2, 3], 1) == [[1], [2], [3]]


def test_window_larger_than_list():
    assert sliding_window([1, 2], 3) == []


def test_empty_list():
    assert sliding_window([], 2) == []


def test_zero_size():
    assert sliding_window([1, 2, 3], 0) == []
