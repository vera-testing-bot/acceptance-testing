def is_palindrome(s: str) -> bool:
    """Return True if s reads the same forwards and backwards (case-insensitive)."""
    normalized = s.lower()
    return normalized == normalized[::-1]
