import re


def word_frequency(text: str) -> dict[str, int]:
    """Return a mapping of each unique word to its frequency in text.

    Words are compared case-insensitively and punctuation is stripped.
    """
    if not text:
        return {}

    words = re.findall(r"[a-zA-Z0-9']+", text.lower())
    # Strip leading/trailing apostrophes from each token
    words = [w.strip("'") for w in words if w.strip("'")]

    freq: dict[str, int] = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq
