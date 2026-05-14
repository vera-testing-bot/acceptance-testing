import pytest

from src.math_utils import (
    add,
    calculate_pepperoni_lbs,
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


def test_calculate_pepperoni_lbs_for_large_pizza():
    assert calculate_pepperoni_lbs(16, 2) == pytest.approx(0.9, rel=0.05)


def test_calculate_pepperoni_lbs_prefers_larger_slices():
    small_slice_lbs = calculate_pepperoni_lbs(16, 1)
    large_slice_lbs = calculate_pepperoni_lbs(16, 2)

    assert small_slice_lbs > large_slice_lbs


def test_calculate_pepperoni_lbs_rejects_non_positive_diameters():
    with pytest.raises(ValueError):
        calculate_pepperoni_lbs(0, 2)

    with pytest.raises(ValueError):
        calculate_pepperoni_lbs(16, -1)
