from src.string_utils import is_palindrome


def test_palindrome_simple():
    assert is_palindrome("racecar") is True


def test_palindrome_single_char():
    assert is_palindrome("a") is True


def test_palindrome_empty():
    assert is_palindrome("") is True


def test_palindrome_case_insensitive():
    assert is_palindrome("Madam") is True


def test_not_palindrome():
    assert is_palindrome("hello") is False


def test_not_palindrome_longer():
    assert is_palindrome("world") is False
