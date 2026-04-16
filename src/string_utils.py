def count_vowels(s: str) -> int:
    """Return the number of vowels (a, e, i, o, u) in the string, case-insensitive."""
    return sum(1 for c in s.lower() if c in "aeiou")


def reverse_words(s: str) -> str:
    """Return the string with the order of words reversed. Words are separated by spaces."""
    return " ".join(s.split()[::-1])
