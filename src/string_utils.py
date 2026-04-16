def capitalize_words(s):
    """Capitalize the first letter of each word in the string."""
    return s.title()


def count_vowels(s):
    """Return the number of vowels (a, e, i, o, u) in the string."""
    return sum(1 for c in s.lower() if c in "aeiou")


def count_consonants(s):
    """Return the number of consonants in the string."""
    return sum(1 for c in s.lower() if c.isalpha() and c not in "aeiou")


def word_count(s):
    """Return the number of words in the string."""
    return len(s.split())


def truncate(s, length):
    """Truncate the string to the given length."""
    return s[:length]


def reverse_words(s):
    """Return the string with the words in reversed order."""
    return " ".join(s.split()[::-1])


def is_pangram(s):
    """Return True if the string contains every letter of the alphabet."""
    return set("abcdefghijklmnopqrstuvwxyz").issubset(set(s.lower()))
