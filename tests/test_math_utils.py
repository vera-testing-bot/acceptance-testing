from src.math_utils import add, negate, is_even, sin


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


def test_sin_known_values_within_tolerance():
    pi = 3.141592653589793
    assert abs(sin(0.0) - 0.0) <= 1e-6
    assert abs(sin(pi / 2) - 1.0) <= 1e-6
    assert abs(sin(-pi / 2) + 1.0) <= 1e-6
    assert abs(sin(pi) - 0.0) <= 1e-6
