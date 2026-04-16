from src.list_utils import is_sorted


def test_sorted_list():
    assert is_sorted([1, 2, 3, 4, 5]) is True


def test_unsorted_list():
    assert is_sorted([3, 1, 2]) is False


def test_empty_list():
    assert is_sorted([]) is True


def test_single_element():
    assert is_sorted([42]) is True


def test_duplicates_sorted():
    assert is_sorted([1, 2, 2, 3]) is True


def test_descending_list():
    assert is_sorted([5, 4, 3, 2, 1]) is False
