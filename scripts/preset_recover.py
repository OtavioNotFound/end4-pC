#!/usr/bin/env python3
"""Explicit config restore. Stop only this shell instance before using it."""
import argparse
import fcntl
from pathlib import Path

from preset_resources import atomic_write, backup, read_object


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot', type=Path, nargs='?')
    parser.add_argument('config', type=Path)
    parser.add_argument('--safe-default', action='store_true', help='explicitly restore empty config using built-in defaults')
    args = parser.parse_args()
    if args.safe_default:
        content = b'{}\n'
    else:
        if args.snapshot is None:
            parser.error('snapshot is required unless --safe-default is selected')
        read_object(args.snapshot)
        content = args.snapshot.read_bytes()
    with args.config.with_suffix('.json.preset.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        # Corrupted current JSON is a primary recovery use case. Back up its
        # exact bytes instead of requiring it to parse before restoration.
        saved = backup(args.config)
        atomic_write(args.config, content)
    print(f'Restored / restaurado; previous config backup / backup anterior: {saved}')


if __name__ == '__main__':
    main()
