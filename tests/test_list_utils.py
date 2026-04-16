from src.list_utils import find_duplicates


def test_find_duplicates_multiple():
    assert find_duplicates([1, 2, 3, 2, 4, 1]) == [2, 1]


def test_find_duplicates_no_duplicates():
    assert find_duplicates([1, 2, 3]) == []


def test_find_duplicates_empty():
    assert find_duplicates([]) == []


def test_find_duplicates_strings():
    assert find_duplicates(['a', 'b', 'a']) == ['a']


def test_find_duplicates_single_element_repeated():
    assert find_duplicates([5, 5, 5]) == [5]


def test_find_duplicates_appears_only_once_in_result():
    assert find_duplicates([1, 1, 1, 2, 2]) == [1, 2]
