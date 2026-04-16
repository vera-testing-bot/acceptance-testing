import pytest

from src.binary_utils import from_binary, to_binary


def test_to_binary_zero():
    assert to_binary(0) == "0"


def test_to_binary_one():
    assert to_binary(1) == "1"


def test_to_binary_positive():
    assert to_binary(5) == "101"
    assert to_binary(10) == "1010"
    assert to_binary(255) == "11111111"


def test_to_binary_negative_raises():
    with pytest.raises(ValueError):
        to_binary(-1)


def test_from_binary_basic():
    assert from_binary("0") == 0
    assert from_binary("1") == 1
    assert from_binary("101") == 5
    assert from_binary("1010") == 10


def test_from_binary_invalid_raises():
    with pytest.raises(ValueError):
        from_binary("2")
    with pytest.raises(ValueError):
        from_binary("abc")
    with pytest.raises(ValueError):
        from_binary("")


def test_round_trip():
    for n in [0, 1, 7, 42, 255, 1024]:
        assert from_binary(to_binary(n)) == n
