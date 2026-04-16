from src.list_utils import flatten


def test_basic_flatten():
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_with_empty_sublist():
    assert flatten([[1], [], [2, 3]]) == [1, 2, 3]


def test_empty_list():
    assert flatten([]) == []


def test_single_sublist():
    assert flatten([[5, 6, 7]]) == [5, 6, 7]
