from src.string_utils import count_vowels, reverse_words


def test_count_vowels_basic():
    assert count_vowels("hello") == 2


def test_count_vowels_empty():
    assert count_vowels("") == 0


def test_count_vowels_no_vowels():
    assert count_vowels("gym") == 0


def test_count_vowels_case_insensitive():
    assert count_vowels("AEIOUaeiou") == 10


def test_reverse_words_two_words():
    assert reverse_words("hello world") == "world hello"


def test_reverse_words_single():
    assert reverse_words("hello") == "hello"


def test_reverse_words_empty():
    assert reverse_words("") == ""


def test_reverse_words_three_words():
    assert reverse_words("one two three") == "three two one"
