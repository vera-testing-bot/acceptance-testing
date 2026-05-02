import math
import pytest

from src.sphere_utils import sphere_volume


def test_sphere_volume_zero_radius():
    assert sphere_volume(0) == 0


def test_sphere_volume_positive_radius():
    assert sphere_volume(3) == pytest.approx(113.09733552923255)


def test_sphere_volume_float_radius():
    assert sphere_volume(2.5) == pytest.approx((4 / 3) * math.pi * (2.5 ** 3))
