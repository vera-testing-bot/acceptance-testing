from src.string_utils import (
    capitalize_words,
    count_vowels,
    count_consonants,
    word_count,
    truncate,
    reverse_words,
    is_pangram,
)


class TestCapitalizeWords:
    def test_basic(self):
        assert capitalize_words("hello world") == "Hello World"

    def test_already_capitalized(self):
        assert capitalize_words("Hello World") == "Hello World"

    def test_empty(self):
        assert capitalize_words("") == ""

    def test_single_word(self):
        assert capitalize_words("python") == "Python"


class TestCountVowels:
    def test_basic(self):
        assert count_vowels("hello") == 2

    def test_no_vowels(self):
        assert count_vowels("gym") == 0

    def test_all_vowels(self):
        assert count_vowels("aeiou") == 5

    def test_empty(self):
        assert count_vowels("") == 0

    def test_case_insensitive(self):
        assert count_vowels("AEIOU") == 5


class TestCountConsonants:
    def test_basic(self):
        assert count_consonants("hello") == 3

    def test_no_consonants(self):
        assert count_consonants("aeiou") == 0

    def test_empty(self):
        assert count_consonants("") == 0

    def test_with_spaces(self):
        assert count_consonants("hello world") == 7

    def test_case_insensitive(self):
        assert count_consonants("HELLO") == 3


class TestWordCount:
    def test_basic(self):
        assert word_count("hello world") == 2

    def test_single_word(self):
        assert word_count("hello") == 1

    def test_empty(self):
        assert word_count("") == 0

    def test_multiple_spaces(self):
        assert word_count("  hello   world  ") == 2


class TestTruncate:
    def test_basic(self):
        assert truncate("hello world", 5) == "hello"

    def test_longer_than_string(self):
        assert truncate("hi", 10) == "hi"

    def test_zero_length(self):
        assert truncate("hello", 0) == ""

    def test_empty_string(self):
        assert truncate("", 5) == ""


class TestReverseWords:
    def test_basic(self):
        assert reverse_words("hello world") == "world hello"

    def test_single_word(self):
        assert reverse_words("hello") == "hello"

    def test_three_words(self):
        assert reverse_words("one two three") == "three two one"

    def test_empty(self):
        assert reverse_words("") == ""


class TestIsPangram:
    def test_pangram(self):
        assert is_pangram("the quick brown fox jumps over the lazy dog") is True

    def test_not_pangram(self):
        assert is_pangram("hello world") is False

    def test_empty(self):
        assert is_pangram("") is False

    def test_case_insensitive(self):
        assert is_pangram("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG") is True
