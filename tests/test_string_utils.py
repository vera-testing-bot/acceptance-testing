from src.string_utils import to_title_case


def test_two_word_string():
    assert to_title_case('hello world') == 'Hello World'


def test_four_word_string():
    assert to_title_case('the quick brown fox') == 'The Quick Brown Fox'


def test_empty_string():
    assert to_title_case('') == ''


def test_mixed_case_string():
    assert to_title_case('already Done') == 'Already Done'
