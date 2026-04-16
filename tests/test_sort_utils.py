from src.sort_utils import bubble_sort


def test_bubble_sort_basic():
    assert bubble_sort([3, 1, 2]) == [1, 2, 3]


def test_bubble_sort_empty():
    assert bubble_sort([]) == []


def test_bubble_sort_single():
    assert bubble_sort([5]) == [5]


def test_bubble_sort_does_not_mutate():
    original = [3, 1, 2]
    bubble_sort(original)
    assert original == [3, 1, 2]
