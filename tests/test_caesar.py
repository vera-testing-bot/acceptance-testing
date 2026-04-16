import pytest
from src.caesar import encrypt, decrypt


def test_basic_encrypt():
    assert encrypt("abc", 1) == "bcd"


def test_basic_decrypt():
    assert decrypt("bcd", 1) == "abc"


def test_wrap_around_encrypt():
    assert encrypt("xyz", 3) == "abc"


def test_wrap_around_decrypt():
    assert decrypt("abc", 3) == "xyz"


def test_mixed_case():
    assert encrypt("Hello", 13) == "Uryyb"
    assert decrypt("Uryyb", 13) == "Hello"


def test_non_alpha_unchanged():
    assert encrypt("Hello, World!", 5) == "Mjqqt, Btwqi!"


def test_roundtrip():
    original = "The quick brown fox jumps over the lazy dog."
    assert decrypt(encrypt(original, 7), 7) == original


def test_zero_shift():
    assert encrypt("abc", 0) == "abc"
    assert decrypt("abc", 0) == "abc"
