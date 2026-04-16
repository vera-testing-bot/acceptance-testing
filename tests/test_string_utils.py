from src.string_utils import count_vowels


def test_count_vowels_typical_word():
    assert count_vowels("hello") == 2


def test_count_vowels_empty_string():
    assert count_vowels("") == 0


def test_count_vowels_no_vowels():
    assert count_vowels("rhythm") == 0


def test_count_vowels_mixed_case():
    assert count_vowels("AeIoU") == 5
