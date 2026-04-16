from src.list_utils import chunk_list


def test_chunk_list_uneven():
    assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_list_exact():
    assert chunk_list([1, 2, 3], 3) == [[1, 2, 3]]


def test_chunk_list_empty():
    assert chunk_list([], 2) == []


def test_chunk_list_even():
    assert chunk_list([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]
