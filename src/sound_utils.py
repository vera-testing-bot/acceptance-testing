SPEED_OF_SOUND_MPS = 343


def distance_at_speed_of_sound(seconds: int | float) -> int | float:
    return seconds * SPEED_OF_SOUND_MPS
