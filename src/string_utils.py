def reverse_words(text: str) -> str:
    """Return the words in text in reversed order.

    >>> reverse_words("hello world")
    'world hello'
    >>> reverse_words("one two three")
    'three two one'
    """
    return " ".join(text.split()[::-1])


def count_consonants(text: str) -> int:
    """Return the number of consonants in text (case-insensitive).

    >>> count_consonants("hello")
    3
    >>> count_consonants("aeiou")
    0
    """
    vowels = set("aeiouAEIOU")
    return sum(1 for ch in text if ch.isalpha() and ch not in vowels)


def title_case(text: str) -> str:
    """Return text converted to title case.

    >>> title_case("hello world")
    'Hello World'
    >>> title_case("the quick brown fox")
    'The Quick Brown Fox'
    """
    return " ".join(word.capitalize() for word in text.split())
