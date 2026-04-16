import pytest

from src.binary_utils import from_binary, to_binary


def test_to_binary_zero():
    assert to_binary(0) == "0"


def test_to_binary_one():
    assert to_binary(1) == "1"


def test_to_binary_powers_of_two():
    assert to_binary(2) == "10"
    assert to_binary(4) == "100"
    assert to_binary(8) == "1000"
    assert to_binary(1024) == "10000000000"


def test_to_binary_arbitrary():
    assert to_binary(5) == "101"
    assert to_binary(10) == "1010"
    assert to_binary(255) == "11111111"


def test_to_binary_no_0b_prefix():
    result = to_binary(42)
    assert not result.startswith("0b")


def test_to_binary_negative_raises():
    with pytest.raises(ValueError):
        to_binary(-1)


def test_from_binary_zero():
    assert from_binary("0") == 0


def test_from_binary_one():
    assert from_binary("1") == 1


def test_from_binary_powers_of_two():
    assert from_binary("10") == 2
    assert from_binary("100") == 4
    assert from_binary("1000") == 8
    assert from_binary("10000000000") == 1024


def test_from_binary_arbitrary():
    assert from_binary("101") == 5
    assert from_binary("1010") == 10
    assert from_binary("11111111") == 255


def test_from_binary_invalid_raises():
    with pytest.raises(ValueError):
        from_binary("2")
    with pytest.raises(ValueError):
        from_binary("abc")
    with pytest.raises(ValueError):
        from_binary("")
    with pytest.raises(ValueError):
        from_binary("102")


def test_round_trip():
    for n in [0, 1, 2, 7, 42, 255, 1000]:
        assert from_binary(to_binary(n)) == n
