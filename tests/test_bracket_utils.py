from src.bracket_utils import is_balanced


def test_nested_parens():
    assert is_balanced("(())") is True


def test_mixed_brackets():
    assert is_balanced("()[]{}") is True


def test_mismatched():
    assert is_balanced("(]") is False


def test_empty_string():
    assert is_balanced("") is True


def test_unmatched_open():
    assert is_balanced("((") is False


def test_complex_balanced():
    assert is_balanced("{[()]}") is True


def test_closing_before_open():
    assert is_balanced(")") is False
