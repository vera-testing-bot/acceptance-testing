from src.box_utils import box_volume


def test_box_volume_positive_values():
    assert box_volume(2, 3, 4) == 24


def test_box_volume_zero_dimension():
    assert box_volume(5, 0, 2) == 0


def test_box_volume_negative_dimension():
    assert box_volume(-2, 3, 4) == -24


def test_box_volume_float_values():
    assert box_volume(1.5, 2, 3) == 9.0
