from src.string_utils import capitalize_words


def test_capitalize_words_basic():
    assert capitalize_words("hello world") == "Hello World"


def test_capitalize_words_already_capitalized():
    assert capitalize_words("Hello World") == "Hello World"


def test_capitalize_words_single_word():
    assert capitalize_words("python") == "Python"


def test_capitalize_words_empty_string():
    assert capitalize_words("") == ""


def test_capitalize_words_multiple_spaces():
    assert capitalize_words("foo  bar") == "Foo  Bar"
