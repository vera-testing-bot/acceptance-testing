from src.truncate import truncate


def test_truncate_returns_text_when_shorter_than_max():
    assert truncate("hi", 10) == "hi"


def test_truncate_returns_text_when_equal_to_max():
    assert truncate("hello", 5) == "hello"


def test_truncate_returns_empty_for_empty_text():
    assert truncate("", 5) == ""


def test_truncate_appends_default_suffix_when_too_long():
    assert truncate("hello world", 8) == "hello..."


def test_truncate_uses_custom_suffix():
    assert truncate("abcdefgh", 5, suffix="…") == "abcd…"


def test_truncate_falls_back_to_slice_when_max_length_le_suffix_length():
    assert truncate("hello world", 2) == "he"
