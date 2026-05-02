from src.sound_utils import distance_at_speed_of_sound


def test_distance_at_speed_of_sound_zero_seconds():
    assert distance_at_speed_of_sound(0) == 0


def test_distance_at_speed_of_sound_positive_seconds():
    assert distance_at_speed_of_sound(10) == 3430


def test_distance_at_speed_of_sound_float_seconds():
    assert distance_at_speed_of_sound(2.5) == 857.5
