from .exceptions import KeyNotFoundError
from .wal import WAL


class KVStore:
    def __init__(self, path):
        self._wal_path = path
        self._data = WAL.replay(path)
        self._wal = WAL(path)

    def get(self, key):
        if key not in self._data:
            raise KeyNotFoundError(key)
        return self._data[key]

    def set(self, key, value):
        self._wal.append(WAL.OP_SET, key, value)
        self._data[key] = value

    def delete(self, key):
        if key not in self._data:
            raise KeyNotFoundError(key)
        self._wal.append(WAL.OP_DELETE, key)
        del self._data[key]

    def keys(self):
        return list(self._data.keys())

    def close(self):
        self._wal.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
