from src.morse import morse_message


def test_morse_message():
    assert morse_message() == "what hath god wrought?"
