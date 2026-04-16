def is_palindrome(s: str) -> bool:
    """Return True if s is a palindrome, ignoring case and spaces."""
    cleaned = s.replace(" ", "").lower()
    return cleaned == cleaned[::-1]
