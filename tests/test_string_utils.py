from src.string_utils import word_count


def test_word_count_two_words():
    assert word_count("hello world") == 2


def test_word_count_one_word():
    assert word_count("one") == 1


def test_word_count_empty_string():
    assert word_count("") == 0


def test_word_count_extra_whitespace():
    assert word_count("  hello   world  ") == 2


def test_word_count_four_words():
    assert word_count("the quick brown fox") == 4
