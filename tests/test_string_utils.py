from src.string_utils import title_case, truncate


def test_title_case_basic():
    assert title_case("hello world") == "Hello World"


def test_title_case_empty():
    assert title_case("") == ""


def test_title_case_all_upper():
    assert title_case("HELLO WORLD") == "Hello World"


def test_title_case_multi_word():
    assert title_case("the quick brown fox") == "The Quick Brown Fox"


def test_truncate_exceeds_limit():
    assert truncate("hello world", 5) == "hello..."


def test_truncate_within_limit():
    assert truncate("hi", 10) == "hi"


def test_truncate_exactly_at_limit():
    assert truncate("hello", 5) == "hello"


def test_truncate_empty_string():
    assert truncate("", 5) == ""
