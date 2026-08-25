def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to at most max_length characters, appending suffix when shortened."""
    if len(text) <= max_length:
        return text
    keep_length = max_length - len(suffix)
    if keep_length <= 0:
        return text[:max_length]
    return text[:keep_length] + suffix
