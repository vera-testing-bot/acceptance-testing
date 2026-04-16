from src.string_utils import is_anagram


def test_anagram_basic():
    assert is_anagram("listen", "silent") is True


def test_anagram_case_insensitive():
    assert is_anagram("Listen", "Silent") is True


def test_anagram_ignores_spaces():
    assert is_anagram("conversation", "voices rant on") is True


def test_not_anagram():
    assert is_anagram("hello", "world") is False


def test_anagram_empty_strings():
    assert is_anagram("", "") is True
