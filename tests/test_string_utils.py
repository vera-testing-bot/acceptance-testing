from src.string_utils import is_palindrome


def test_palindrome_simple():
    assert is_palindrome("racecar") is True


def test_palindrome_ignores_case():
    assert is_palindrome("RaceCar") is True


def test_palindrome_ignores_spaces():
    assert is_palindrome("race car") is True


def test_palindrome_phrase():
    assert is_palindrome("A man a plan a canal Panama") is True


def test_not_palindrome():
    assert is_palindrome("hello") is False


def test_empty_string():
    assert is_palindrome("") is True


def test_single_character():
    assert is_palindrome("a") is True
