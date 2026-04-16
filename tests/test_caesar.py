import pytest
from src.caesar import encrypt, decrypt


def test_encrypt_basic_lowercase():
    assert encrypt("hello", 3) == "khoor"


def test_encrypt_basic_uppercase():
    assert encrypt("HELLO", 3) == "KHOOR"


def test_encrypt_mixed_case():
    assert encrypt("Hello", 3) == "Khoor"


def test_encrypt_wrap_around():
    assert encrypt("xyz", 3) == "abc"


def test_encrypt_uppercase_wrap():
    assert encrypt("XYZ", 3) == "ABC"


def test_encrypt_preserves_spaces():
    assert encrypt("hello world", 1) == "ifmmp xpsme"


def test_encrypt_preserves_punctuation():
    assert encrypt("hello, world!", 1) == "ifmmp, xpsme!"


def test_encrypt_zero_shift():
    assert encrypt("hello", 0) == "hello"


def test_encrypt_full_rotation():
    assert encrypt("hello", 26) == "hello"


def test_encrypt_negative_shift():
    assert encrypt("khoor", -3) == "hello"


def test_decrypt_basic():
    assert decrypt("khoor", 3) == "hello"


def test_decrypt_uppercase():
    assert decrypt("KHOOR", 3) == "HELLO"


def test_roundtrip():
    original = "Hello, World!"
    assert decrypt(encrypt(original, 13), 13) == original


def test_roundtrip_large_shift():
    original = "The quick brown fox"
    assert decrypt(encrypt(original, 7), 7) == original
