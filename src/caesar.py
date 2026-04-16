def encrypt(text: str, shift: int) -> str:
    """Encrypt text using a Caesar cipher with the given shift.

    Letters are shifted by `shift` positions in the alphabet (wrapping around).
    Non-alphabetic characters are passed through unchanged.
    """
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


def decrypt(text: str, shift: int) -> str:
    """Decrypt text that was encrypted with a Caesar cipher using the given shift."""
    return encrypt(text, -shift)
