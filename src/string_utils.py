def to_title_case(s: str) -> str:
    """Convert a string so the first letter of each word is capitalised and the rest lowercase."""
    return " ".join(word.capitalize() for word in s.split(" ")) if s else s


def truncate(s: str, max_len: int) -> str:
    """Return s truncated to at most max_len characters.

    If truncated, the result ends with '...' (counted within max_len).
    """
    if len(s) <= max_len:
        return s
    return s[: max(0, max_len - 3)] + "..."
