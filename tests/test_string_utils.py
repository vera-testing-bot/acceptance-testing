from src.string_utils import to_title_case, truncate


def test_to_title_case_basic():
    assert to_title_case("hello world") == "Hello World"


def test_to_title_case_sentence():
    assert to_title_case("the quick brown fox") == "The Quick Brown Fox"


def test_to_title_case_empty():
    assert to_title_case("") == ""


def test_to_title_case_mixed():
    assert to_title_case("already Done") == "Already Done"


def test_truncate_needs_truncation():
    assert truncate("hello world", 8) == "hello..."


def test_truncate_no_truncation():
    assert truncate("hi", 10) == "hi"


def test_truncate_exact_fit():
    assert truncate("hello", 5) == "hello"


def test_truncate_very_short_max():
    assert truncate("abcdef", 3) == "..."


def test_truncate_empty():
    assert truncate("", 5) == ""
