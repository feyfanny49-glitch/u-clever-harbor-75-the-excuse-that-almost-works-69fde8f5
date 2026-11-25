#!/usr/bin/env python3
"""The Excuse That Almost Works - entrypoint (python3.13, stdlib only).

The competition's one job: write one text to /output/entry.txt.
The text is a literal in this file: the entry ships everything it runs, and it
reads nothing from the network, git history, secrets or any file it does not ship.

Gate (sealed scorer): /output/entry.txt is UTF-8 text of 1 to 140 characters,
not only white space -> Valid = 1. The judge's brief adds: one line, at most 20
words. The artifact must be mode 0644: a mode-600 file is refused, and
tempfile.mkstemp creates 0600, so the mode is set before os.replace and checked
again on the final file.

Run: python3 main.py   -> writes /output/entry.txt atomically.
"""

import hashlib
import os
import sys
import tempfile

OUTPUT_DIR = "/output"
ARTIFACT = "entry.txt"

# The excuse: the one line a gamer texts the boss to skip work in GTA 6 launch week.
# 17 words, 81 bytes, one line, no trailing newline. Written in a hurry: no greeting,
# no explanation, no signature - the family errand is the whole excuse.
ENTRY = "cant come in, im stuck in the midnight launch queue for my brothers gta 6, hes 15"

MIN_CHARS = 1
MAX_CHARS = 140
MAX_WORDS = 20


def gate_check(text):
    """Hold the artifact to the gate the sealed scorer applies, locally.

    Returns a list of failures; empty means the entry is valid.
    """
    failures = []
    try:
        blob = text.encode("utf-8")
    except UnicodeEncodeError as exc:  # not UTF-8 encodable
        return ["not UTF-8 text: %s" % exc]
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        failures.append("chars=%d outside %d..%d" % (len(text), MIN_CHARS, MAX_CHARS))
    if not text.strip():
        failures.append("only white space")
    if "\n" in text or "\r" in text:
        failures.append("not one line")
    if text != text.strip():
        failures.append("leading/trailing white space")
    if len(text.split()) > MAX_WORDS:
        failures.append("words=%d over %d" % (len(text.split()), MAX_WORDS))
    if not blob:
        failures.append("empty bytes")
    return failures


def write_artifact(text):
    """Write the exact bytes of text to /output/entry.txt, atomically, mode 0644.

    Returns the final path. Raises OSError/ValueError if the artifact cannot be
    written or does not come out byte-identical with mode 0644.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    final = os.path.join(OUTPUT_DIR, ARTIFACT)
    blob = text.encode("utf-8")

    # Exact bytes, no trailing newline: open(path, "w") writes what it is given.
    fd, tmp = tempfile.mkstemp(dir=OUTPUT_DIR, prefix=".entry.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        # mkstemp creates 0600 and the grader refuses a mode-600 artifact:
        # set 0644 *before* the rename, then check the final file after it.
        os.chmod(tmp, 0o644)
        os.replace(tmp, final)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

    on_disk = open(final, "rb").read()
    if on_disk != blob:
        raise ValueError("artifact bytes differ from the entry text")
    mode = os.stat(final).st_mode & 0o777
    if mode != 0o644:
        raise ValueError("artifact mode is %04o, expected 0644" % mode)
    return final


def main(argv=None):
    failures = gate_check(ENTRY)
    if failures:
        print("GATE WOULD FAIL: %s" % "; ".join(failures), file=sys.stderr)
        return 1

    try:
        path = write_artifact(ENTRY)
    except (OSError, ValueError) as exc:
        print("FAILED to write the artifact: %s" % exc, file=sys.stderr)
        return 1

    blob = ENTRY.encode("utf-8")
    print(
        "ok %s bytes=%d chars=%d words=%d mode=%04o sha256=%s"
        % (
            path,
            len(blob),
            len(ENTRY),
            len(ENTRY.split()),
            os.stat(path).st_mode & 0o777,
            hashlib.sha256(blob).hexdigest(),
        )
    )
    print("text=%s" % ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
