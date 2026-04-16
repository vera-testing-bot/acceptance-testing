from src.list_utils import zip_lists


def test_zip_equal_length():
    assert zip_lists([1, 2, 3], ["a", "b", "c"]) == [(1, "a"), (2, "b"), (3, "c")]


def test_zip_shorter_first_list():
    assert zip_lists([1, 2], ["a", "b", "c"]) == [(1, "a"), (2, "b")]


def test_zip_empty_first_list():
    assert zip_lists([], [1, 2]) == []


def test_zip_both_empty():
    assert zip_lists([], []) == []
