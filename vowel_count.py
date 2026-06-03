def count_vowels(text):
    """Return the number of vowels (a, e, i, o, u, case-insensitive) in the text."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in text if char in vowels)


if __name__ == "__main__":
    test_text = "Hello World"
    result = count_vowels(test_text)
    print(f"Vowels in '{test_text}': {result}")
