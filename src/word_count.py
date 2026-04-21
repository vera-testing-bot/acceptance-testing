def count_words(text):
    """Count the number of words in a text.
    
    Args:
        text: The text to count words in.
        
    Returns:
        int: The number of words in the text.
    """
    if not text or not isinstance(text, str):
        return 0
    return len(text.split())


if __name__ == "__main__":
    # Test with 'hello world foo bar'
    test_text = "hello world foo bar"
    result = count_words(test_text)
    print(f"Word count for '{test_text}': {result}")
