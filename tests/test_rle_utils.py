from src.rle_utils import rle_decode, rle_encode


def test_encode_basic():
    assert rle_encode('aaabbc') == '3a2b1c'


def test_decode_basic():
    assert rle_decode('3a2b1c') == 'aaabbc'


def test_encode_empty():
    assert rle_encode('') == ''


def test_decode_empty():
    assert rle_decode('') == ''


def test_encode_single_char():
    assert rle_encode('a') == '1a'


def test_encode_no_repeats():
    assert rle_encode('abc') == '1a1b1c'


def test_decode_multi_digit_count():
    assert rle_decode('12a') == 'a' * 12


def test_roundtrip_basic():
    assert rle_decode(rle_encode('aaabbc')) == 'aaabbc'


def test_roundtrip_single():
    assert rle_decode(rle_encode('z')) == 'z'


def test_roundtrip_all_same():
    assert rle_decode(rle_encode('aaaaaaa')) == 'aaaaaaa'


def test_roundtrip_no_repeats():
    assert rle_decode(rle_encode('abcde')) == 'abcde'
