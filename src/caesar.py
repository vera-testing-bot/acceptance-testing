def encrypt(text, shift):
    """Encrypt text using Caesar cipher with the given shift."""
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def decrypt(text, shift):
    """Decrypt text using Caesar cipher with the given shift."""
    return encrypt(text, -shift)
