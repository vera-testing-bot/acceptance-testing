from src.word_frequency import word_frequency


def test_empty_string():
    assert word_frequency("") == {}


def test_single_word():
    assert word_frequency("hello") == {"hello": 1}


def test_repeated_words():
    assert word_frequency("hello world hello") == {"hello": 2, "world": 1}


def test_mixed_case():
    assert word_frequency("Hello HELLO hello") == {"hello": 3}


def test_punctuation_stripped():
    assert word_frequency("hello, world! hello.") == {"hello": 2, "world": 1}


def test_multiple_unique_words():
    result = word_frequency("the quick brown fox")
    assert result == {"the": 1, "quick": 1, "brown": 1, "fox": 1}


def test_mixed_case_and_punctuation():
    result = word_frequency("It's great, it's really great!")
    assert result["great"] == 2
