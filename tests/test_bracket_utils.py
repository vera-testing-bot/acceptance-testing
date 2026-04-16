from src.bracket_utils import is_balanced


def test_nested_parens():
    assert is_balanced('(())') is True


def test_mixed_brackets():
    assert is_balanced('()[]{}') is True


def test_mismatched_brackets():
    assert is_balanced('(]') is False


def test_empty_string():
    assert is_balanced('') is True


def test_nested_mixed():
    assert is_balanced('{[()]}') is True


def test_unmatched_open():
    assert is_balanced('(') is False


def test_unmatched_close():
    assert is_balanced(')') is False


def test_non_bracket_chars():
    assert is_balanced('a(b)c') is True


def test_single_open_bracket():
    assert is_balanced('[') is False


def test_single_close_bracket():
    assert is_balanced('}') is False
