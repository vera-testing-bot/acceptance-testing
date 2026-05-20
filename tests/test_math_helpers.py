import pytest
import math

from src.math_helpers import (
    AVOGADRO_CONSTANT_PER_MOL,
    EARTH_GRAVITY_M_PER_S2,
    GRAVITATIONAL_CONSTANT_M3_PER_KG_S2,
    PHYSICS_CONSTANTS,
    PLANCK_CONSTANT_J_S,
    SPEED_OF_LIGHT,
    SPEED_OF_LIGHT_KM_PER_S,
    SPEED_OF_LIGHT_M_PER_S,
    SPEED_OF_LIGHT_MI_PER_S,
    calculate_sphere_volume,
    physics_constant,
    divide,
    factorial,
    multiply,
    speed_of_light,
)


def test_multiply_positive():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(5, 0) == 0


def test_multiply_negative():
    assert multiply(-2, 3) == -6


def test_multiply_floats():
    assert multiply(2.5, 4) == 10.0


def test_divide_basic():
    assert divide(10, 2) == 5.0


def test_divide_negative():
    assert divide(-9, 3) == -3.0


def test_divide_floats():
    assert divide(7.5, 2.5) == 3.0


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(5, 0)


def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_one():
    assert factorial(1) == 1


def test_factorial_positive():
    assert factorial(5) == 120


def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-1)


def test_calculate_sphere_volume_zero_radius():
    assert calculate_sphere_volume(0) == 0.0


def test_calculate_sphere_volume_positive_radius():
    assert calculate_sphere_volume(3) == pytest.approx(113.09733552923255)


def test_calculate_sphere_volume_negative_radius():
    with pytest.raises(ValueError):
        calculate_sphere_volume(-1)


def test_speed_of_light_constants_in_multiple_units():
    assert SPEED_OF_LIGHT_M_PER_S == 299_792_458
    assert SPEED_OF_LIGHT_KM_PER_S == 299_792.458
    assert math.isclose(SPEED_OF_LIGHT_MI_PER_S, 186_282.39705122002)


def test_speed_of_light_mapping():
    assert SPEED_OF_LIGHT["m/s"] == SPEED_OF_LIGHT_M_PER_S
    assert SPEED_OF_LIGHT["km/s"] == SPEED_OF_LIGHT_KM_PER_S
    assert SPEED_OF_LIGHT["mi/s"] == SPEED_OF_LIGHT_MI_PER_S


def test_speed_of_light_returns_value_for_unit():
    assert speed_of_light("m/s") == SPEED_OF_LIGHT_M_PER_S
    assert speed_of_light("km/s") == SPEED_OF_LIGHT_KM_PER_S
    assert speed_of_light("mi/s") == SPEED_OF_LIGHT_MI_PER_S


def test_speed_of_light_rejects_unsupported_unit():
    with pytest.raises(ValueError, match="Unsupported unit"):
        speed_of_light("ft/s")


def test_physics_constants_include_core_values():
    assert math.isclose(EARTH_GRAVITY_M_PER_S2, 9.80665, rel_tol=1e-12, abs_tol=0.0)
    assert math.isclose(
        GRAVITATIONAL_CONSTANT_M3_PER_KG_S2,
        6.67430e-11,
        rel_tol=1e-12,
        abs_tol=0.0,
    )
    assert math.isclose(PLANCK_CONSTANT_J_S, 6.62607015e-34, rel_tol=1e-12, abs_tol=0.0)
    assert math.isclose(AVOGADRO_CONSTANT_PER_MOL, 6.02214076e23, rel_tol=1e-12, abs_tol=0.0)


def test_physics_constant_mapping():
    assert PHYSICS_CONSTANTS["gravity"] == EARTH_GRAVITY_M_PER_S2
    assert PHYSICS_CONSTANTS["gravitational_constant"] == GRAVITATIONAL_CONSTANT_M3_PER_KG_S2
    assert PHYSICS_CONSTANTS["planck_constant"] == PLANCK_CONSTANT_J_S
    assert PHYSICS_CONSTANTS["avogadro_constant"] == AVOGADRO_CONSTANT_PER_MOL


def test_physics_constant_returns_value_for_name():
    assert physics_constant("gravity") == EARTH_GRAVITY_M_PER_S2
    assert physics_constant("gravitational_constant") == GRAVITATIONAL_CONSTANT_M3_PER_KG_S2
    assert physics_constant("planck_constant") == PLANCK_CONSTANT_J_S
    assert physics_constant("avogadro_constant") == AVOGADRO_CONSTANT_PER_MOL


def test_physics_constant_rejects_unsupported_name():
    with pytest.raises(ValueError, match="Unsupported constant"):
        physics_constant("pi")
