from src.math_utils import add, is_power_of_two


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 5) == 5


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_is_power_of_two_one():
    assert is_power_of_two(1) is True


def test_is_power_of_two_two():
    assert is_power_of_two(2) is True


def test_is_power_of_two_eight():
    assert is_power_of_two(8) is True


def test_is_power_of_two_zero():
    assert is_power_of_two(0) is False


def test_is_power_of_two_six():
    assert is_power_of_two(6) is False


def test_is_power_of_two_negative():
    assert is_power_of_two(-4) is False
