def count_consonants(s: str) -> int:
    """Count the number of consonants in a string (case-insensitive)."""
    vowels = set("aeiou")
    return sum(1 for c in s.lower() if c.isalpha() and c not in vowels)
