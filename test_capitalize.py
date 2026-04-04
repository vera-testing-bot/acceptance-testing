from capitalize import capitalize_words


def test_single_word():
    assert capitalize_words("hello") == "Hello"


def test_multiple_words():
    assert capitalize_words("hello world") == "Hello World"


def test_empty_string():
    assert capitalize_words("") == ""


def test_already_capitalized():
    assert capitalize_words("Hello World") == "Hello World"


def test_mixed_case():
    assert capitalize_words("hElLo wOrLd") == "Hello World"


def test_single_character_words():
    assert capitalize_words("a b c") == "A B C"


def test_apostrophe_preserved():
    assert capitalize_words("it's a test") == "It's A Test"
