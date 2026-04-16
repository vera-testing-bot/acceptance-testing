from src.string_utils import is_pangram


def test_is_pangram_classic():
    assert is_pangram("The quick brown fox jumps over the lazy dog") is True


def test_is_pangram_false():
    assert is_pangram("Hello world") is False


def test_is_pangram_empty():
    assert is_pangram("") is False


def test_is_pangram_pack():
    assert is_pangram("Pack my box with five dozen liquor jugs") is True
