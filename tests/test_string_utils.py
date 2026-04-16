from src.string_utils import reverse_words


def test_two_words():
    assert reverse_words("hello world") == "world hello"


def test_single_word():
    assert reverse_words("hello") == "hello"


def test_empty_string():
    assert reverse_words("") == ""


def test_three_word_sentence():
    assert reverse_words("one two three") == "three two one"
