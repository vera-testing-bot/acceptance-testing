def is_leap_year(year: int) -> bool:
    """Return True if year is a leap year, False otherwise.

    A year is a leap year if divisible by 4, except centuries unless also divisible by 400.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
