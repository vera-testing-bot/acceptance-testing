from src.string_utils import count_consonants


def test_count_consonants_basic():
    assert count_consonants("hello") == 3


def test_count_consonants_case_insensitive():
    assert count_consonants("Hello World") == 7


def test_count_consonants_empty_string():
    assert count_consonants("") == 0


def test_count_consonants_vowels_only():
    assert count_consonants("aeiou") == 0


def test_count_consonants_digits_and_punctuation():
    assert count_consonants("123!@#") == 0


def test_count_consonants_mixed():
    assert count_consonants("abc123!") == 2
