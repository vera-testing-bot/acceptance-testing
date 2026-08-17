import time
from .exceptions import CorruptedWALError

_SENTINEL = object()


def escape(s):
    """Escape pipe, backslash, and newline characters for WAL encoding."""
    return s.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "\\n")


def unescape(s):
    """Reverse the escaping applied by :func:`escape`."""
    result = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == "|":
                result.append("|")
            elif nxt == "n":
                result.append("\n")
            elif nxt == "\\":
                result.append("\\")
            else:
                result.append(s[i])
                result.append(nxt)
            i += 2
        else:
            result.append(s[i])
            i += 1
    return "".join(result)


class WAL:
    """Append-only write-ahead log. Each entry: timestamp|op|key|value\n"""

    OP_SET = "SET"
    OP_DELETE = "DELETE"

    def __init__(self, path):
        self.path = path
        self._file = open(path, "a", encoding="utf-8")

    def append(self, op, key, value=""):
        timestamp = f"{time.time():.6f}"
        safe_key = escape(key)
        safe_value = escape(value)
        line = f"{timestamp}|{op}|{safe_key}|{safe_value}\n"
        self._file.write(line)
        self._file.flush()

    def close(self):
        self._file.close()

    @staticmethod
    def _unescape(s):
        return unescape(s)

    @classmethod
    def replay(cls, path):
        """Replay WAL file and return dict of current state (no tombstones)."""
        state = {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return state

        for lineno, raw in enumerate(lines, start=1):
            line = raw.rstrip("\n")
            if not line:
                continue
            parts = cls._split_line(line)
            if parts is None or len(parts) != 4:
                raise CorruptedWALError(lineno, raw.rstrip("\n"))
            _ts, op, key_escaped, value_escaped = parts
            if op not in (cls.OP_SET, cls.OP_DELETE):
                raise CorruptedWALError(lineno, raw.rstrip("\n"))
            key = cls._unescape(key_escaped)
            value = cls._unescape(value_escaped)
            if op == cls.OP_SET:
                state[key] = value
            elif op == cls.OP_DELETE:
                state.pop(key, None)

        return state

    @classmethod
    def _split_line(cls, line):
        """Split on unescaped '|', expecting exactly 4 parts."""
        parts = []
        current = []
        i = 0
        while i < len(line):
            if line[i] == "\\" and i + 1 < len(line):
                current.append(line[i])
                current.append(line[i + 1])
                i += 2
            elif line[i] == "|":
                parts.append("".join(current))
                current = []
                i += 1
            else:
                current.append(line[i])
                i += 1
        parts.append("".join(current))
        return parts if len(parts) == 4 else None
