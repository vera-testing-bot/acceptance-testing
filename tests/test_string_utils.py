from src.string_utils import truncate


def test_truncate_basic():
    assert truncate('hello world', 8) == 'hello...'


def test_truncate_no_truncation_needed():
    assert truncate('hi', 10) == 'hi'


def test_truncate_exact_fit():
    assert truncate('hello', 5) == 'hello'


def test_truncate_short_max_len():
    assert truncate('abcdef', 3) == '...'


def test_truncate_empty_string():
    assert truncate('', 5) == ''
