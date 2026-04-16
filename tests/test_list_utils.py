from src.list_utils import flatten


def test_flatten_already_flat():
    assert flatten([1, 2, 3]) == [1, 2, 3]


def test_flatten_single_level_nesting():
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_flatten_deeply_nested():
    assert flatten([1, [2, [3, [4]]]]) == [1, 2, 3, 4]


def test_flatten_empty():
    assert flatten([]) == []


def test_flatten_empty_nested():
    assert flatten([[], [], []]) == []


def test_flatten_mixed_types():
    assert flatten([1, "a", [2, "b", [3, "c"]]]) == [1, "a", 2, "b", 3, "c"]
