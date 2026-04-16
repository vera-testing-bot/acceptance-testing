from src.rle_utils import rle_encode, rle_decode


def test_encode_basic():
    assert rle_encode("aaabbc") == "3a2b1c"


def test_decode_basic():
    assert rle_decode("3a2b1c") == "aaabbc"


def test_encode_empty():
    assert rle_encode("") == ""


def test_decode_empty():
    assert rle_decode("") == ""


def test_encode_no_repeats():
    assert rle_encode("abc") == "1a1b1c"


def test_round_trip():
    s = "aabbccddee"
    assert rle_decode(rle_encode(s)) == s


def test_round_trip_no_repeats():
    s = "hello"
    assert rle_decode(rle_encode(s)) == s
