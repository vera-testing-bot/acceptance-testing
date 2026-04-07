import os
import pytest
from src.kvstore.store import KVStore
from src.kvstore.exceptions import KeyNotFoundError


@pytest.fixture
def wal_path(tmp_path):
    return str(tmp_path / "test.wal")


def test_set_and_get(wal_path):
    with KVStore(wal_path) as store:
        store.set("foo", "bar")
        assert store.get("foo") == "bar"


def test_get_missing_key_raises(wal_path):
    with KVStore(wal_path) as store:
        with pytest.raises(KeyNotFoundError):
            store.get("missing")


def test_overwrite_key(wal_path):
    with KVStore(wal_path) as store:
        store.set("x", "1")
        store.set("x", "2")
        assert store.get("x") == "2"


def test_delete_key(wal_path):
    with KVStore(wal_path) as store:
        store.set("k", "v")
        store.delete("k")
        with pytest.raises(KeyNotFoundError):
            store.get("k")


def test_delete_missing_key_raises(wal_path):
    with KVStore(wal_path) as store:
        with pytest.raises(KeyNotFoundError):
            store.delete("nope")


def test_keys(wal_path):
    with KVStore(wal_path) as store:
        store.set("a", "1")
        store.set("b", "2")
        store.set("c", "3")
        assert sorted(store.keys()) == ["a", "b", "c"]


def test_keys_excludes_deleted(wal_path):
    with KVStore(wal_path) as store:
        store.set("a", "1")
        store.set("b", "2")
        store.delete("a")
        assert store.keys() == ["b"]


def test_persistence_across_restart(wal_path):
    with KVStore(wal_path) as store:
        store.set("name", "alice")
        store.set("city", "paris")

    # Reopen — should replay WAL and restore state
    with KVStore(wal_path) as store:
        assert store.get("name") == "alice"
        assert store.get("city") == "paris"


def test_delete_persisted_across_restart(wal_path):
    with KVStore(wal_path) as store:
        store.set("name", "alice")
        store.delete("name")

    with KVStore(wal_path) as store:
        with pytest.raises(KeyNotFoundError):
            store.get("name")
        assert store.keys() == []


def test_tombstone_semantics(wal_path):
    """Deleted key can be re-set after deletion."""
    with KVStore(wal_path) as store:
        store.set("k", "v1")
        store.delete("k")
        store.set("k", "v2")
        assert store.get("k") == "v2"


def test_context_manager(wal_path):
    with KVStore(wal_path) as store:
        store.set("cm", "yes")
    # WAL file should exist after close
    assert os.path.exists(wal_path)


def test_empty_store_keys(wal_path):
    with KVStore(wal_path) as store:
        assert store.keys() == []


def test_special_characters_in_key_value(wal_path):
    with KVStore(wal_path) as store:
        store.set("key|with|pipes", "val|ue")
        assert store.get("key|with|pipes") == "val|ue"

    with KVStore(wal_path) as store:
        assert store.get("key|with|pipes") == "val|ue"
