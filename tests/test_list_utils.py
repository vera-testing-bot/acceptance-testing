from src.list_utils import rotate_list


def test_rotate_by_two():
    assert rotate_list([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]


def test_rotate_by_zero():
    assert rotate_list([1, 2, 3], 0) == [1, 2, 3]


def test_rotate_full_rotation():
    assert rotate_list([1, 2, 3], 3) == [1, 2, 3]


def test_rotate_empty_list():
    assert rotate_list([], 2) == []


def test_rotate_k_greater_than_len():
    assert rotate_list([1, 2, 3], 5) == rotate_list([1, 2, 3], 2)
