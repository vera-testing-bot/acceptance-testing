import os
import time

from .wal import WAL, escape


def compact(wal_path):
    """Compact the WAL: write only latest values to a temp file, then atomically replace."""
    state = WAL.replay(wal_path)

    tmp_path = wal_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        # Write a single SET entry per surviving key using a fixed timestamp
        ts = f"{time.time():.6f}"
        for key, value in state.items():
            safe_key = escape(key)
            safe_value = escape(value)
            f.write(f"{ts}|{WAL.OP_SET}|{safe_key}|{safe_value}\n")

    os.replace(tmp_path, wal_path)
    return len(state)
