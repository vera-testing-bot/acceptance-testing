def is_anagram(s1: str, s2: str) -> bool:
    """Return True if s1 and s2 are anagrams of each other.

    Comparison is case-insensitive and ignores spaces.
    """
    normalize = lambda s: sorted(s.lower().replace(" ", ""))
    return normalize(s1) == normalize(s2)
