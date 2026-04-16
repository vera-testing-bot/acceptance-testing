import pytest
from src.seq_utils import nth_fibonacci


def test_fibonacci_zero():
    assert nth_fibonacci(0) == 0


def test_fibonacci_one():
    assert nth_fibonacci(1) == 1


def test_fibonacci_seven():
    assert nth_fibonacci(7) == 13


def test_fibonacci_ten():
    assert nth_fibonacci(10) == 55


def test_fibonacci_negative_raises():
    with pytest.raises(ValueError):
        nth_fibonacci(-1)
