from src.string_utils import is_pangram, word_count


# is_pangram tests
def test_is_pangram_true():
    assert is_pangram("The quick brown fox jumps over the lazy dog") is True


def test_is_pangram_false():
    assert is_pangram("Hello world") is False


def test_is_pangram_empty():
    assert is_pangram("") is False


def test_is_pangram_another_pangram():
    assert is_pangram("Pack my box with five dozen liquor jugs") is True


def test_is_pangram_mixed_case():
    assert is_pangram("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG") is True


# word_count tests
def test_word_count_two_words():
    assert word_count("hello world") == 2


def test_word_count_one_word():
    assert word_count("one") == 1


def test_word_count_empty():
    assert word_count("") == 0


def test_word_count_extra_spaces():
    assert word_count("  hello   world  ") == 2


def test_word_count_four_words():
    assert word_count("the quick brown fox") == 4
