from src.list_utils import remove_duplicates


def test_remove_duplicates_basic():
    assert remove_duplicates([1, 2, 2, 3]) == [1, 2, 3]


def test_remove_duplicates_preserves_order():
    assert remove_duplicates([3, 1, 2, 1, 3]) == [3, 1, 2]


def test_remove_duplicates_no_duplicates():
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]


def test_remove_duplicates_empty():
    assert remove_duplicates([]) == []


def test_remove_duplicates_strings():
    assert remove_duplicates(["a", "b", "a"]) == ["a", "b"]
