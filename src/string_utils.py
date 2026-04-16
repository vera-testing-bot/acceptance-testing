def reverse_words(s: str) -> str:
    words = s.split(" ")
    return " ".join(reversed(words))
