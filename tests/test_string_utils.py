from src.string_utils import count_vowels


def test_count_vowels_basic():
    assert count_vowels("hello") == 2


def test_count_vowels_uppercase():
    assert count_vowels("HELLO") == 2


def test_count_vowels_mixed_case():
    assert count_vowels("HeLLo WoRLd") == 3


def test_count_vowels_empty_string():
    assert count_vowels("") == 0


def test_count_vowels_no_vowels():
    assert count_vowels("bcdfg") == 0


def test_count_vowels_special_characters():
    assert count_vowels("h3ll0 w0rld!") == 0


def test_count_vowels_all_vowels():
    assert count_vowels("aeiou") == 5
