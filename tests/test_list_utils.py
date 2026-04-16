from src.list_utils import flatten, is_sorted, rotate_list, zip_lists


# flatten tests
def test_flatten_basic():
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_flatten_with_empty_sublist():
    assert flatten([[1, 2], [], [3]]) == [1, 2, 3]


def test_flatten_empty():
    assert flatten([]) == []


def test_flatten_single_sublist():
    assert flatten([[1, 2, 3]]) == [1, 2, 3]


# is_sorted tests
def test_is_sorted_sorted():
    assert is_sorted([1, 2, 3]) is True


def test_is_sorted_unsorted():
    assert is_sorted([3, 1, 2]) is False


def test_is_sorted_empty():
    assert is_sorted([]) is True


def test_is_sorted_single():
    assert is_sorted([5]) is True


def test_is_sorted_duplicates():
    assert is_sorted([1, 1, 2]) is True


# rotate_list tests
def test_rotate_list_basic():
    assert rotate_list([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]


def test_rotate_list_zero():
    assert rotate_list([1, 2, 3], 0) == [1, 2, 3]


def test_rotate_list_full():
    assert rotate_list([1, 2, 3], 3) == [1, 2, 3]


def test_rotate_list_empty():
    assert rotate_list([], 2) == []


def test_rotate_list_k_greater_than_len():
    assert rotate_list([1, 2, 3], 5) == rotate_list([1, 2, 3], 2)


# zip_lists tests
def test_zip_lists_equal_length():
    assert zip_lists([1, 2, 3], ["a", "b", "c"]) == [(1, "a"), (2, "b"), (3, "c")]


def test_zip_lists_first_shorter():
    assert zip_lists([1, 2], ["a", "b", "c"]) == [(1, "a"), (2, "b")]


def test_zip_lists_first_empty():
    assert zip_lists([], [1, 2]) == []


def test_zip_lists_both_empty():
    assert zip_lists([], []) == []
