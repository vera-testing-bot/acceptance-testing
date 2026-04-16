from src.search_utils import binary_search


def test_found_middle():
    assert binary_search([1, 3, 5, 7], 5) == 2


def test_not_found():
    assert binary_search([1, 3, 5, 7], 4) == -1


def test_empty_list():
    assert binary_search([], 1) == -1


def test_found_first():
    assert binary_search([2, 4, 6, 8], 2) == 0


def test_found_last():
    assert binary_search([2, 4, 6, 8], 8) == 3


def test_single_element_found():
    assert binary_search([7], 7) == 0


def test_single_element_not_found():
    assert binary_search([7], 3) == -1
