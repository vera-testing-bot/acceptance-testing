import pytest

from src.math_utils import add, average, clamp, is_prime, factorial


class TestAdd:
    def test_add_positive(self):
        assert add(2, 3) == 5

    def test_add_negative(self):
        assert add(-1, -2) == -3

    def test_add_zero(self):
        assert add(0, 5) == 5


class TestAverage:
    def test_basic(self):
        assert average([1, 2, 3, 4, 5]) == 3.0

    def test_single_element(self):
        assert average([7]) == 7.0

    def test_floats(self):
        assert average([1.0, 2.0, 3.0]) == 2.0

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            average([])


class TestClamp:
    def test_within_range(self):
        assert clamp(5, 0, 10) == 5

    def test_below_min(self):
        assert clamp(-5, 0, 10) == 0

    def test_above_max(self):
        assert clamp(15, 0, 10) == 10

    def test_at_min(self):
        assert clamp(0, 0, 10) == 0

    def test_at_max(self):
        assert clamp(10, 0, 10) == 10


class TestIsPrime:
    def test_negative(self):
        assert is_prime(-1) is False

    def test_zero(self):
        assert is_prime(0) is False

    def test_one(self):
        assert is_prime(1) is False

    def test_two(self):
        assert is_prime(2) is True

    def test_three(self):
        assert is_prime(3) is True

    def test_four(self):
        assert is_prime(4) is False

    def test_large_prime(self):
        assert is_prime(97) is True

    def test_large_composite(self):
        assert is_prime(100) is False


class TestFactorial:
    def test_zero(self):
        assert factorial(0) == 1

    def test_one(self):
        assert factorial(1) == 1

    def test_five(self):
        assert factorial(5) == 120

    def test_ten(self):
        assert factorial(10) == 3628800

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            factorial(-1)
