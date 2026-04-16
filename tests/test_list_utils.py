from src.list_utils import (
    sum_list,
    product_list,
    flatten,
    is_sorted,
    chunk_list,
    deduplicate,
    zip_lists,
    sliding_window,
)


class TestSumList:
    def test_sum_integers(self):
        assert sum_list([1, 2, 3, 4]) == 10

    def test_sum_empty(self):
        assert sum_list([]) == 0

    def test_sum_negatives(self):
        assert sum_list([-1, -2, -3]) == -6

    def test_sum_floats(self):
        assert sum_list([1.5, 2.5]) == 4.0


class TestProductList:
    def test_product_integers(self):
        assert product_list([1, 2, 3, 4]) == 24

    def test_product_empty(self):
        assert product_list([]) == 1

    def test_product_with_zero(self):
        assert product_list([1, 2, 0, 4]) == 0

    def test_product_negatives(self):
        assert product_list([-2, 3]) == -6


class TestFlatten:
    def test_flatten_nested(self):
        assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    def test_flatten_mixed(self):
        assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

    def test_flatten_empty(self):
        assert flatten([]) == []

    def test_flatten_already_flat(self):
        assert flatten([1, 2, 3]) == [1, 2, 3]


class TestIsSorted:
    def test_sorted_ascending(self):
        assert is_sorted([1, 2, 3, 4]) is True

    def test_not_sorted(self):
        assert is_sorted([1, 3, 2, 4]) is False

    def test_empty(self):
        assert is_sorted([]) is True

    def test_single_element(self):
        assert is_sorted([5]) is True

    def test_equal_elements(self):
        assert is_sorted([3, 3, 3]) is True


class TestChunkList:
    def test_even_chunks(self):
        assert chunk_list([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_uneven_chunks(self):
        assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_empty_list(self):
        assert chunk_list([], 3) == []

    def test_chunk_larger_than_list(self):
        assert chunk_list([1, 2], 5) == [[1, 2]]


class TestDeduplicate:
    def test_removes_duplicates(self):
        assert deduplicate([1, 2, 2, 3, 3, 3]) == [1, 2, 3]

    def test_preserves_order(self):
        assert deduplicate([3, 1, 2, 1, 3]) == [3, 1, 2]

    def test_empty(self):
        assert deduplicate([]) == []

    def test_no_duplicates(self):
        assert deduplicate([1, 2, 3]) == [1, 2, 3]


class TestZipLists:
    def test_equal_length(self):
        assert zip_lists([1, 2, 3], ["a", "b", "c"]) == [(1, "a"), (2, "b"), (3, "c")]

    def test_truncates_to_shorter(self):
        assert zip_lists([1, 2, 3], ["a", "b"]) == [(1, "a"), (2, "b")]

    def test_empty_lists(self):
        assert zip_lists([], []) == []


class TestSlidingWindow:
    def test_basic_window(self):
        assert sliding_window([1, 2, 3, 4], 2) == [[1, 2], [2, 3], [3, 4]]

    def test_window_equals_list(self):
        assert sliding_window([1, 2, 3], 3) == [[1, 2, 3]]

    def test_window_larger_than_list(self):
        assert sliding_window([1, 2], 5) == []

    def test_empty_list(self):
        assert sliding_window([], 2) == []
