from src.math_utils import (
    add,
    hello_spec_audit,
    hello_spec_audit_1778114263,
    is_even,
    is_kaprekar_number,
    is_perfect_number,
    negate,
)


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 5) == 5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_negate_positive():
    assert negate(5) == -5


def test_negate_negative():
    assert negate(-2) == 2


def test_negate_zero():
    assert negate(0) == 0


def test_is_even_true():
    assert is_even(2) is True


def test_is_even_false():
    assert is_even(3) is False


def test_is_even_zero():
    assert is_even(0) is True


def test_is_perfect_number_cases():
    assert is_perfect_number(6) is True
    assert is_perfect_number(28) is True
    assert is_perfect_number(12) is False
    assert is_perfect_number(1) is False
    assert is_perfect_number(-5) is False
    assert is_perfect_number(0) is False


def test_is_kaprekar_number_cases():
    assert is_kaprekar_number(1) is True
    assert is_kaprekar_number(9) is True
    assert is_kaprekar_number(45) is True
    assert is_kaprekar_number(10) is False
    assert is_kaprekar_number(-45) is False


def test_hello_spec_audit_1778114263_returns_42():
    assert hello_spec_audit_1778114263() == 42


def test_hello_spec_audit_returns_42():
    assert hello_spec_audit() == 42
