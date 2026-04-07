import os
import pytest
from src.kvstore.store import KVStore
from src.kvstore.compactor import compact
from src.kvstore.wal import WAL
from src.kvstore.exceptions import KeyNotFoundError


@pytest.fixture
def wal_path(tmp_path):
    return str(tmp_path / "test.wal")


def test_compact_reduces_file_size(wal_path):
    with KVStore(wal_path) as store:
        for i in range(20):
            store.set("key", f"value_{i}")  # 20 writes to same key

    size_before = os.path.getsize(wal_path)
    compact(wal_path)
    size_after = os.path.getsize(wal_path)

    assert size_after < size_before


def test_compact_preserves_data(wal_path):
    with KVStore(wal_path) as store:
        store.set("a", "1")
        store.set("b", "2")
        store.set("a", "updated")

    compact(wal_path)

    with KVStore(wal_path) as store:
        assert store.get("a") == "updated"
        assert store.get("b") == "2"


def test_compact_removes_tombstones(wal_path):
    with KVStore(wal_path) as store:
        store.set("gone", "value")
        store.delete("gone")
        store.set("kept", "yes")

    compact(wal_path)

    with KVStore(wal_path) as store:
        with pytest.raises(KeyNotFoundError):
            store.get("gone")
        assert store.get("kept") == "yes"
        assert store.keys() == ["kept"]


def test_compact_deleted_keys_not_in_wal(wal_path):
    with KVStore(wal_path) as store:
        store.set("x", "1")
        store.delete("x")

    compact(wal_path)

    # Raw WAL file should not contain deleted key
    with open(wal_path) as f:
        content = f.read()
    assert "x" not in content


def test_compact_empty_store(wal_path):
    with KVStore(wal_path) as store:
        store.set("k", "v")
        store.delete("k")

    n = compact(wal_path)
    assert n == 0
    assert os.path.getsize(wal_path) == 0


def test_compact_returns_key_count(wal_path):
    with KVStore(wal_path) as store:
        store.set("a", "1")
        store.set("b", "2")
        store.set("c", "3")

    n = compact(wal_path)
    assert n == 3


def test_compact_is_atomic(wal_path):
    """Compaction uses a temp file and rename — original is only replaced on success."""
    with KVStore(wal_path) as store:
        store.set("safe", "data")

    compact(wal_path)

    # Temp file should not remain
    assert not os.path.exists(wal_path + ".tmp")
    # Data should still be readable
    with KVStore(wal_path) as store:
        assert store.get("safe") == "data"


def test_compact_multiple_times(wal_path):
    with KVStore(wal_path) as store:
        store.set("x", "1")

    compact(wal_path)

    with KVStore(wal_path) as store:
        store.set("x", "2")
        store.set("y", "3")

    compact(wal_path)

    with KVStore(wal_path) as store:
        assert store.get("x") == "2"
        assert store.get("y") == "3"


def test_compact_preserves_special_chars(wal_path):
    with KVStore(wal_path) as store:
        store.set("k|ey", "va|lue")

    compact(wal_path)

    with KVStore(wal_path) as store:
        assert store.get("k|ey") == "va|lue"
