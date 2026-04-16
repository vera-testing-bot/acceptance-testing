from src.anagram import is_anagram


def test_true_anagram():
    assert is_anagram("listen", "silent") is True


def test_true_anagram_with_spaces():
    assert is_anagram("a gentleman", "elegant man") is True


def test_non_anagram():
    assert is_anagram("hello", "world") is False


def test_non_anagram_different_lengths():
    assert is_anagram("abc", "ab") is False


def test_case_insensitive():
    assert is_anagram("Listen", "Silent") is True


def test_case_insensitive_mixed():
    assert is_anagram("Triangle", "Integral") is True


def test_empty_strings():
    assert is_anagram("", "") is True


def test_empty_vs_nonempty():
    assert is_anagram("", "a") is False
