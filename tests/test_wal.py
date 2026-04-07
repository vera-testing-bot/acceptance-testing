import pytest
from src.kvstore.wal import WAL
from src.kvstore.exceptions import CorruptedWALError


@pytest.fixture
def wal_path(tmp_path):
    return str(tmp_path / "test.wal")


def test_replay_empty_file(wal_path):
    open(wal_path, "w").close()
    assert WAL.replay(wal_path) == {}


def test_replay_missing_file(wal_path):
    # File does not exist — should return empty dict
    assert WAL.replay(wal_path + ".missing") == {}


def test_replay_set_entries(wal_path):
    wal = WAL(wal_path)
    wal.append(WAL.OP_SET, "a", "1")
    wal.append(WAL.OP_SET, "b", "2")
    wal.close()

    state = WAL.replay(wal_path)
    assert state == {"a": "1", "b": "2"}


def test_replay_overwrite(wal_path):
    wal = WAL(wal_path)
    wal.append(WAL.OP_SET, "x", "old")
    wal.append(WAL.OP_SET, "x", "new")
    wal.close()

    assert WAL.replay(wal_path) == {"x": "new"}


def test_replay_delete_removes_key(wal_path):
    wal = WAL(wal_path)
    wal.append(WAL.OP_SET, "k", "v")
    wal.append(WAL.OP_DELETE, "k")
    wal.close()

    assert WAL.replay(wal_path) == {}


def test_replay_delete_nonexistent_key_is_noop(wal_path):
    wal = WAL(wal_path)
    wal.append(WAL.OP_DELETE, "ghost")
    wal.close()

    assert WAL.replay(wal_path) == {}


def test_corrupted_wal_truncated_line(wal_path):
    with open(wal_path, "w") as f:
        f.write("1234567890|SET|key\n")  # missing value field

    with pytest.raises(CorruptedWALError) as exc_info:
        WAL.replay(wal_path)
    assert exc_info.value.line_number == 1


def test_corrupted_wal_invalid_op(wal_path):
    with open(wal_path, "w") as f:
        f.write("1234567890|INVALID|key|value\n")

    with pytest.raises(CorruptedWALError) as exc_info:
        WAL.replay(wal_path)
    assert exc_info.value.line_number == 1


def test_corrupted_wal_reports_correct_line_number(wal_path):
    with open(wal_path, "w") as f:
        f.write("1.000000|SET|a|1\n")
        f.write("2.000000|SET|b|2\n")
        f.write("bad line\n")  # line 3

    with pytest.raises(CorruptedWALError) as exc_info:
        WAL.replay(wal_path)
    assert exc_info.value.line_number == 3


def test_replay_order_matters(wal_path):
    """Later entries should win over earlier ones."""
    wal = WAL(wal_path)
    wal.append(WAL.OP_SET, "k", "first")
    wal.append(WAL.OP_SET, "k", "second")
    wal.append(WAL.OP_SET, "k", "third")
    wal.close()

    assert WAL.replay(wal_path)["k"] == "third"


def test_replay_pipe_in_key_value(wal_path):
    wal = WAL(wal_path)
    wal.append(WAL.OP_SET, "k|ey", "va|lue")
    wal.close()

    state = WAL.replay(wal_path)
    assert state == {"k|ey": "va|lue"}


def test_blank_lines_ignored(wal_path):
    with open(wal_path, "w") as f:
        f.write("1.000000|SET|a|1\n")
        f.write("\n")
        f.write("2.000000|SET|b|2\n")

    state = WAL.replay(wal_path)
    assert state == {"a": "1", "b": "2"}
