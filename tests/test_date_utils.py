from src.date_utils import is_leap_year


def test_divisible_by_400():
    assert is_leap_year(2000) is True


def test_century_not_divisible_by_400():
    assert is_leap_year(1900) is False


def test_divisible_by_4_not_century():
    assert is_leap_year(2024) is True


def test_not_divisible_by_4():
    assert is_leap_year(2023) is False
