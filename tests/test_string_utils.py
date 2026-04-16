from src.string_utils import truncate


def test_truncate_longer_string():
    assert truncate("hello world", 5) == "hello..."


def test_truncate_shorter_string():
    assert truncate("hi", 10) == "hi"


def test_truncate_exact_limit():
    assert truncate("hello", 5) == "hello"


def test_truncate_empty_string():
    assert truncate("", 5) == ""
