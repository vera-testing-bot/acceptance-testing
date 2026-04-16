from src.string_utils import title_case


def test_title_case_basic():
    assert title_case("hello world") == "Hello World"


def test_title_case_empty_string():
    assert title_case("") == ""


def test_title_case_all_uppercase():
    assert title_case("HELLO WORLD") == "Hello World"


def test_title_case_multiple_words():
    assert title_case("the quick brown fox") == "The Quick Brown Fox"
