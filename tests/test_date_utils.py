from src.date_utils import is_leap_year


def test_leap_year_divisible_by_400():
    assert is_leap_year(2000) is True


def test_not_leap_year_century_not_divisible_by_400():
    assert is_leap_year(1900) is False


def test_leap_year_divisible_by_4():
    assert is_leap_year(2024) is True


def test_not_leap_year_not_divisible_by_4():
    assert is_leap_year(2023) is False
