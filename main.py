"""Write the competition entry: one commit message to /output/entry.txt.

The entry is a single line, at most 100 characters, that reads like a real
commit message for a bug fix that made everything worse: the crash on
startup was fixed by removing startup, so the app can no longer crash --
because it no longer starts.
"""

import os

ENTRY = "fix: crash on startup by removing startup"

MAX_CHARS = 100


def validate(line):
    """Check the line against the gate: UTF-8, 1-100 chars, one line."""
    if not line or line.strip() == "":
        raise ValueError("entry must not be empty or only whitespace")
    if len(line) != len(line.strip()):
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_CHARS} cap")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("entry must not contain control characters")
    data = line.encode("utf-8")
    if data.decode("utf-8") != line:
        raise ValueError("entry failed its UTF-8 round-trip")
    return data


def main():
    data = validate(ENTRY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)

    # Re-read and verify the bytes on disk match exactly, and re-check the
    # gate on what was actually written (char count + no trailing newline).
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("entry.txt on disk does not match the entry")
    if written.endswith(b"\n"):
        raise ValueError("entry.txt must not end with a newline")
    if not 1 <= len(written.decode("utf-8")) <= MAX_CHARS:
        raise ValueError("entry.txt fails the 1-100 character gate")
    print(f"wrote {len(data)} bytes to {path}")


if __name__ == "__main__":
    main()
