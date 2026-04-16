from src.list_utils import find_duplicates


def test_find_duplicates_basic():
    assert find_duplicates([1, 2, 3, 2, 4, 1]) == [2, 1]


def test_find_duplicates_no_duplicates():
    assert find_duplicates([1, 2, 3]) == []


def test_find_duplicates_empty():
    assert find_duplicates([]) == []


def test_find_duplicates_strings():
    assert find_duplicates(["a", "b", "a"]) == ["a"]
