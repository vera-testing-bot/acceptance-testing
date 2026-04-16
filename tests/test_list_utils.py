from src.list_utils import rotate_list, group_by


def test_rotate_list_basic():
    assert rotate_list([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]


def test_rotate_list_by_zero():
    assert rotate_list([1, 2, 3], 0) == [1, 2, 3]


def test_rotate_list_full_rotation():
    assert rotate_list([1, 2, 3], 3) == [1, 2, 3]


def test_rotate_list_empty():
    assert rotate_list([], 2) == []


def test_group_by_basic():
    result = group_by([1, 2, 3, 4], lambda x: x % 2)
    assert result == {0: [2, 4], 1: [1, 3]}


def test_group_by_strings():
    result = group_by(["cat", "car", "dog"], lambda s: s[0])
    assert result == {"c": ["cat", "car"], "d": ["dog"]}


def test_group_by_empty():
    assert group_by([], lambda x: x) == {}


def test_group_by_single_group():
    result = group_by([1, 2, 3], lambda x: "all")
    assert result == {"all": [1, 2, 3]}
