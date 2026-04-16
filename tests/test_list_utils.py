from src.list_utils import remove_duplicates


def test_remove_duplicates_preserves_order():
    assert remove_duplicates([1, 2, 2, 3, 1]) == [1, 2, 3]


def test_remove_duplicates_empty():
    assert remove_duplicates([]) == []


def test_remove_duplicates_all_same():
    assert remove_duplicates([1, 1, 1]) == [1]


def test_remove_duplicates_no_duplicates():
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]


def test_remove_duplicates_mixed_types():
    assert remove_duplicates([1, "a", 1, "a", 2]) == [1, "a", 2]
