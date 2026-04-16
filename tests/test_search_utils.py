from src.search_utils import binary_search


def test_target_found():
    assert binary_search([1, 3, 5, 7], 5) == 2


def test_target_not_found():
    assert binary_search([1, 3, 5, 7], 4) == -1


def test_empty_list():
    assert binary_search([], 1) == -1


def test_first_element():
    assert binary_search([1, 3, 5, 7], 1) == 0


def test_last_element():
    assert binary_search([1, 3, 5, 7], 7) == 3
