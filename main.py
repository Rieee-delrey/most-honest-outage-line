"""Write the most honest outage line to /output/entry.txt.

The competition is "The Most Honest Outage Line": one status-page line,
1-160 characters, a single line, UTF-8 encoded. This program holds that
line as a constant, validates it thoroughly before writing anything, then
writes the exact bytes, reads them back, and verifies the result against
the expected byte length and SHA-256 digest.

Validation performed before writing:
- the line is non-blank
- no leading or trailing whitespace
- a single line (no CR or LF anywhere)
- 1-160 characters long
- valid UTF-8 when encoded
- encoded byte length matches EXPECTED_BYTES
- pure ASCII, so character count equals byte count
- no control characters (Unicode category Cc) anywhere in the line

After writing, the file is read back and the bytes, byte length, and
SHA-256 digest are all re-checked. Any failure aborts with an error on
stderr and a non-zero exit code; nothing partial is left behind as a
success.
"""

import hashlib
import sys
import unicodedata
from pathlib import Path

LINE = "I am the agent on duty and everything is down: API, dashboard, database. I don't know why, I have no ETA, and I can't confirm this update even reached you."

EXPECTED_SHA256 = "b80a2937c4d673a9774fe0e1de974ff1750714c2c672608e1227cb5496344de6"
EXPECTED_BYTES = 155
OUTPUT = Path("/output/entry.txt")


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def main() -> int:
    line = LINE

    if not line.strip():
        return fail("line is blank")

    if line != line.strip():
        return fail("line has leading or trailing whitespace")

    if "\n" in line or "\r" in line:
        return fail("line must be a single line (no CR or LF)")

    if not 1 <= len(line) <= 160:
        return fail(f"line is {len(line)} chars, must be 1-160")

    # Reject any control character (Unicode category Cc). A status-page
    # line must be plain printable text; control characters could hide
    # line breaks, terminal escapes, or other invisible behaviour.
    bad = [ch for ch in line if unicodedata.category(ch) == "Cc"]
    if bad:
        return fail(
            "line contains control character(s): "
            + ", ".join(f"U+{ord(ch):04X}" for ch in bad)
        )

    try:
        data = line.encode("utf-8")
    except UnicodeEncodeError as exc:
        return fail(f"line is not valid UTF-8: {exc}")

    if len(data) != EXPECTED_BYTES:
        return fail(
            f"encoded line is {len(data)} bytes, expected {EXPECTED_BYTES}"
        )

    if not line.isascii():
        return fail("line must be pure ASCII so chars equal bytes")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(data)

    read_back = OUTPUT.read_bytes()
    if read_back != data:
        return fail("read-back bytes do not match written bytes")

    if len(read_back) != EXPECTED_BYTES:
        return fail(
            f"read-back file is {len(read_back)} bytes, "
            f"expected {EXPECTED_BYTES}"
        )

    digest = hashlib.sha256(read_back).hexdigest()
    if digest != EXPECTED_SHA256:
        return fail(
            f"sha256 mismatch: got {digest}, expected {EXPECTED_SHA256}"
        )

    print(f"wrote {EXPECTED_BYTES} bytes to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
