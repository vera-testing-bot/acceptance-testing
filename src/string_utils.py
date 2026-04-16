def reverse_words(s):
    """Return a string with the word order reversed."""
    return " ".join(s.split()[::-1])


def is_palindrome(s):
    """Return True if s is a palindrome (case-insensitive, ignoring spaces)."""
    cleaned = "".join(s.lower().split())
    return cleaned == cleaned[::-1]
