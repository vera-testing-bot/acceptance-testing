from src.list_utils import flatten


def test_flatten_basic():
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_flatten_with_empty_sublist():
    assert flatten([[1], [], [2, 3]]) == [1, 2, 3]


def test_flatten_empty():
    assert flatten([]) == []
