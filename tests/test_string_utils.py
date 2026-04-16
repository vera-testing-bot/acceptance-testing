from src.string_utils import is_palindrome


def test_is_palindrome_true():
    assert is_palindrome("racecar") is True


def test_is_palindrome_false():
    assert is_palindrome("hello") is False


def test_is_palindrome_with_spaces():
    assert is_palindrome("race car") is True


def test_is_palindrome_case_insensitive():
    assert is_palindrome("Racecar") is True


def test_is_palindrome_empty():
    assert is_palindrome("") is True


def test_is_palindrome_single_char():
    assert is_palindrome("a") is True
