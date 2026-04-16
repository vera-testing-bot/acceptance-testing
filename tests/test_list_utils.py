from src.list_utils import product_list


def test_product_empty_list():
    assert product_list([]) == 1


def test_product_single_element():
    assert product_list([5]) == 5


def test_product_multiple_elements():
    assert product_list([2, 3, 4]) == 24


def test_product_with_zero():
    assert product_list([1, 2, 0, 4]) == 0


def test_product_negative_numbers():
    assert product_list([-1, -2, 3]) == 6


def test_product_floats():
    assert product_list([1.5, 2.0]) == 3.0
