import pytest

from src.roman_numeral import to_roman


def test_single_digit():
    assert to_roman(1) == "I"
    assert to_roman(5) == "V"


def test_subtractive_forms():
    assert to_roman(4) == "IV"
    assert to_roman(9) == "IX"
    assert to_roman(40) == "XL"
    assert to_roman(90) == "XC"
    assert to_roman(400) == "CD"
    assert to_roman(900) == "CM"


def test_additive_forms():
    assert to_roman(3) == "III"
    assert to_roman(8) == "VIII"


def test_large_number():
    assert to_roman(2024) == "MMXXIV"
    assert to_roman(3999) == "MMMCMXCIX"


def test_out_of_range_raises():
    with pytest.raises(ValueError):
        to_roman(0)
    with pytest.raises(ValueError):
        to_roman(4000)
    with pytest.raises(ValueError):
        to_roman(-1)
