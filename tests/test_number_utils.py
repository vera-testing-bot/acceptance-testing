from src.number_utils import number_to_words


def test_zero():
    assert number_to_words(0) == "zero"


def test_forty_two():
    assert number_to_words(42) == "forty two"


def test_one_hundred():
    assert number_to_words(100) == "one hundred"


def test_nine_hundred_ninety_nine():
    assert number_to_words(999) == "nine hundred ninety nine"


def test_teens():
    assert number_to_words(13) == "thirteen"


def test_exact_tens():
    assert number_to_words(50) == "fifty"


def test_two_hundred_twenty_one():
    assert number_to_words(221) == "two hundred twenty one"
