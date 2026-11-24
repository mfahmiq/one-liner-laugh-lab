#!/usr/bin/env python3
"""One-Liner Laugh Lab — make.fun entry.

Writes a single funny line (74 characters, within the 1-200 gate): the
excuse a robot vacuum gives after eating a sock.

Python 3.13, standard library only, deterministic, no network.
The output file is written to $MAKEFUN_OUTPUT_DIR/entry.txt.
"""

import os
import sys

ENTRY = (
    "Per my warranty, socks left on the floor are legally classified as snacks."
)


def main() -> int:
    if not 1 <= len(ENTRY) <= 200:
        print(f"entry must be 1-200 chars, got {len(ENTRY)}", file=sys.stderr)
        return 1
    if ENTRY != ENTRY.strip() or "\n" in ENTRY:
        print("entry must be a single non-padded line", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
