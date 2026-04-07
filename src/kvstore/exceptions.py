class KeyNotFoundError(KeyError):
    def __init__(self, key):
        super().__init__(key)
        self.key = key

    def __str__(self):
        return f"Key not found: {self.key!r}"


class CorruptedWALError(Exception):
    def __init__(self, line_number, line=None):
        self.line_number = line_number
        self.line = line
        msg = f"Corrupted WAL entry at line {line_number}"
        if line is not None:
            msg += f": {line!r}"
        super().__init__(msg)
