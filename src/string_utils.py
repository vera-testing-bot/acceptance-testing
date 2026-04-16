def is_pangram(s):
    """Return True if s contains every letter of the alphabet (case-insensitive)."""
    return set("abcdefghijklmnopqrstuvwxyz").issubset(set(s.lower()))


def word_count(s):
    """Return the number of words in s (split by whitespace)."""
    return len(s.split())
