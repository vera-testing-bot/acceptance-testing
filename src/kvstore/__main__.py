import sys
from .store import KVStore
from .compactor import compact
from .exceptions import KeyNotFoundError

DEFAULT_PATH = "kvstore.wal"


def usage():
    print("Usage:")
    print("  python -m kvstore get KEY [--store PATH]")
    print("  python -m kvstore set KEY VALUE [--store PATH]")
    print("  python -m kvstore compact [--store PATH]")
    sys.exit(1)


def main():
    args = list(sys.argv[1:])

    # Parse optional --store flag
    store_path = DEFAULT_PATH
    if "--store" in args:
        idx = args.index("--store")
        if idx + 1 >= len(args):
            print("Error: --store requires a path argument", file=sys.stderr)
            sys.exit(1)
        store_path = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    if not args:
        usage()

    cmd = args[0]

    if cmd == "get":
        if len(args) != 2:
            usage()
        key = args[1]
        with KVStore(store_path) as store:
            try:
                print(store.get(key))
            except KeyNotFoundError:
                print(f"Error: key {key!r} not found", file=sys.stderr)
                sys.exit(1)

    elif cmd == "set":
        if len(args) != 3:
            usage()
        key, value = args[1], args[2]
        with KVStore(store_path) as store:
            store.set(key, value)

    elif cmd == "compact":
        n = compact(store_path)
        print(f"Compacted to {n} keys.")

    else:
        usage()


if __name__ == "__main__":
    main()
