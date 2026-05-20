from vowel_count import count_vowels


def test_count_vowels_counts_mixed_case_text():
    assert count_vowels("Hello World") == 3


def test_count_vowels_returns_zero_for_empty_string():
    assert count_vowels("") == 0


def test_count_vowels_returns_zero_for_punctuation_only():
    assert count_vowels("?!,.;:-") == 0
