from src.string_utils import reverse_words, is_palindrome


def test_reverse_words_basic():
    assert reverse_words("hello world") == "world hello"


def test_reverse_words_single_word():
    assert reverse_words("hello") == "hello"


def test_reverse_words_multiple():
    assert reverse_words("one two three") == "three two one"


def test_reverse_words_empty():
    assert reverse_words("") == ""


def test_is_palindrome_simple():
    assert is_palindrome("racecar") is True


def test_is_palindrome_with_spaces():
    assert is_palindrome("race car") is True


def test_is_palindrome_case_insensitive():
    assert is_palindrome("Racecar") is True


def test_is_palindrome_not_palindrome():
    assert is_palindrome("hello") is False
