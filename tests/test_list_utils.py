from src.list_utils import deduplicate


def test_deduplicate_removes_duplicates():
    assert deduplicate([1, 2, 2, 3, 1]) == [1, 2, 3]


def test_deduplicate_empty():
    assert deduplicate([]) == []


def test_deduplicate_all_same():
    assert deduplicate([1, 1, 1]) == [1]


def test_deduplicate_no_duplicates():
    assert deduplicate([1, 2, 3]) == [1, 2, 3]
