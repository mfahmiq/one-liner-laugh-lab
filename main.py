#!/usr/bin/env python3
"""One-Liner Laugh Lab — make.fun entry.

Writes a single funny line (74 characters, within the 1-200 gate): the
excuse a robot vacuum gives after eating a sock.

The joke: a robot vacuum does not apologise like a person; it cites
paperwork. "Per my warranty" is the voice of a machine that has read its
own terms and conditions and found a loophole, and the twist lands on the
very last word — the sock was not stolen, it was *classified*. The blame
quietly lands on the owner, too: the sock was *left on the floor*, so
under the rules the vacuum did nothing wrong. Deadpan legalistic voice,
fresh angle (no hunger, no "it looked delicious"), one breath long.

The sealed gate checks /output/entry.txt is UTF-8 text of 1 to 200
characters, not only white space. This program enforces the same gate
itself before writing — length, single line, no leading/trailing padding,
no trailing newline — and then reads the file back and verifies it is
byte-for-byte identical to the entry, so a bad write can never slip
through silently.

Python 3.13, standard library only, deterministic, no network.
The output file is written to $MAKEFUN_OUTPUT_DIR/entry.txt.
"""

import os
import sys

ENTRY = (
    "Per my warranty, socks left on the floor are legally classified as snacks."
)


def validate(entry: str) -> str | None:
    """Return an error message if *entry* fails the gate, else None."""
    if not 1 <= len(entry) <= 200:
        return f"entry must be 1-200 chars, got {len(entry)}"
    if entry != entry.strip():
        return "entry must not have leading or trailing padding"
    if "\n" in entry or "\r" in entry:
        return "entry must be a single line"
    if not entry.strip():
        return "entry must not be only white space"
    return None


def write_entry(entry: str, out_dir: str) -> str:
    """Write *entry* to ``<out_dir>/entry.txt`` and verify the round trip."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    with open(path, "rb") as f:
        written = f.read()
    if written != entry.encode("utf-8"):
        raise RuntimeError(
            f"verification failed: {path} does not match the entry "
            f"({len(written)} bytes written, {len(entry.encode('utf-8'))} expected)"
        )
    return path


def main() -> int:
    error = validate(ENTRY)
    if error is not None:
        print(error, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    try:
        path = write_entry(ENTRY, out_dir)
    except (OSError, RuntimeError) as exc:
        print(f"failed to write entry: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {len(ENTRY)}-char entry to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
