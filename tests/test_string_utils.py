import pytest
from src.string_utils import reverse_words, count_consonants, title_case


class TestReverseWords:
    def test_two_words(self):
        assert reverse_words("hello world") == "world hello"

    def test_three_words(self):
        assert reverse_words("one two three") == "three two one"

    def test_single_word(self):
        assert reverse_words("hello") == "hello"

    def test_extra_whitespace_ignored(self):
        assert reverse_words("  foo  bar  ") == "bar foo"


class TestCountConsonants:
    def test_basic(self):
        assert count_consonants("hello") == 3

    def test_all_vowels(self):
        assert count_consonants("aeiou") == 0

    def test_mixed(self):
        # p, y, t, h, n are all consonants → 5
        assert count_consonants("python") == 5

    def test_case_insensitive(self):
        assert count_consonants("Hello") == count_consonants("hello")

    def test_non_alpha_ignored(self):
        # h, l, l are consonants; digits and punctuation are ignored → 3
        assert count_consonants("h3ll0!") == 3


class TestTitleCase:
    def test_basic(self):
        assert title_case("hello world") == "Hello World"

    def test_multiple_words(self):
        assert title_case("the quick brown fox") == "The Quick Brown Fox"

    def test_single_word(self):
        assert title_case("python") == "Python"

    def test_already_title(self):
        assert title_case("Hello World") == "Hello World"
