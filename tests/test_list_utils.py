from src.list_utils import zip_lists


def test_zip_equal_length():
    assert zip_lists([1, 2, 3], ["a", "b", "c"]) == [(1, "a"), (2, "b"), (3, "c")]


def test_zip_empty_lists():
    assert zip_lists([], []) == []


def test_zip_unequal_length():
    assert zip_lists([1, 2, 3], ["a", "b"]) == [(1, "a"), (2, "b")]
