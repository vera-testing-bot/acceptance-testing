from src.vowel_counter import count_vowels


def test_basic_string():
    assert count_vowels("hello") == 2


def test_all_vowels():
    assert count_vowels("aeiou") == 5


def test_no_vowels():
    assert count_vowels("gym") == 0


def test_empty_string():
    assert count_vowels("") == 0


def test_uppercase():
    assert count_vowels("HELLO") == 2


def test_mixed_case():
    assert count_vowels("HeLLo WoRLd") == 3


def test_numbers_and_punctuation():
    assert count_vowels("h3ll0!") == 0
