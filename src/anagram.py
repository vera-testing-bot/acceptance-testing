def is_anagram(s1: str, s2: str) -> bool:
    normalize = lambda s: sorted(s.lower().replace(" ", ""))
    return normalize(s1) == normalize(s2)
