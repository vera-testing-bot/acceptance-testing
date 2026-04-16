import pytest
from src.roman_numeral import to_roman


class TestSingleDigits:
    def test_one(self):
        assert to_roman(1) == "I"

    def test_four(self):
        assert to_roman(4) == "IV"

    def test_five(self):
        assert to_roman(5) == "V"

    def test_nine(self):
        assert to_roman(9) == "IX"


class TestTens:
    def test_ten(self):
        assert to_roman(10) == "X"

    def test_forty(self):
        assert to_roman(40) == "XL"

    def test_fifty(self):
        assert to_roman(50) == "L"

    def test_ninety(self):
        assert to_roman(90) == "XC"


class TestHundreds:
    def test_one_hundred(self):
        assert to_roman(100) == "C"

    def test_four_hundred(self):
        assert to_roman(400) == "CD"

    def test_five_hundred(self):
        assert to_roman(500) == "D"

    def test_nine_hundred(self):
        assert to_roman(900) == "CM"


class TestThousands:
    def test_one_thousand(self):
        assert to_roman(1000) == "M"

    def test_three_thousand(self):
        assert to_roman(3000) == "MMM"

    def test_max_value(self):
        assert to_roman(3999) == "MMMCMXCIX"


class TestLargerNumbers:
    def test_2024(self):
        assert to_roman(2024) == "MMXXIV"

    def test_1994(self):
        assert to_roman(1994) == "MCMXCIV"

    def test_58(self):
        assert to_roman(58) == "LVIII"

    def test_1776(self):
        assert to_roman(1776) == "MDCCLXXVI"


class TestErrorCases:
    def test_zero_raises(self):
        with pytest.raises(ValueError):
            to_roman(0)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            to_roman(-1)

    def test_too_large_raises(self):
        with pytest.raises(ValueError):
            to_roman(4000)

    def test_float_raises(self):
        with pytest.raises((ValueError, TypeError)):
            to_roman(1.5)  # type: ignore

    def test_bool_raises(self):
        with pytest.raises(ValueError):
            to_roman(True)  # type: ignore
