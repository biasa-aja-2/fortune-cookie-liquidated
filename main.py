"""Fortune Cookie for the Liquidated Trader.

Writes one fortune-cookie line for a crypto trader who has just been
liquidated, to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

The line is judged pairwise by a model playing the freshly liquidated
trader: it must read as a real fortune, land its joke on the loss, stay
rueful and warm (never cruel or smug), and carry a fresh turn. This one
does it with a double meaning: "risk-free" is every trader's dream, and
here it is achieved the worst possible way -- by having nothing left to
lose.
"""

import os
import sys

TEXT = "Good news: your portfolio is now 100% risk-free. It contains nothing."

MAX_CHARS = 160  # sealed scorer gate: /output/entry.txt, 1-160 chars
MAX_WORDS = 20  # judge brief: at most 20 words of plain text


def gate(text):
    """Check the line against the bounty gate and the judge brief."""
    if not isinstance(text, str):
        return "not text"
    text.encode("utf-8")  # raises on non-UTF-8
    if not (1 <= len(text) <= MAX_CHARS):
        return "length %d outside 1-%d chars" % (len(text), MAX_CHARS)
    if not text.strip():
        return "only whitespace"
    if text != text.strip():
        return "leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return "more than one line"
    if any(ord(ch) < 32 for ch in text):
        return "control character"
    words = text.split()
    if len(words) > MAX_WORDS:
        return "%d words, over the %d-word limit" % (len(words), MAX_WORDS)
    return None


def main():
    problem = gate(TEXT)
    if problem is not None:
        print("refusing to write: %s" % problem, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(TEXT)
    os.chmod(path, 0o644)
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != TEXT.encode("utf-8"):
        print("read-back mismatch", file=sys.stderr)
        return 1
    problem = gate(raw.decode("utf-8"))
    if problem is not None:
        print("read-back failed gate: %s" % problem, file=sys.stderr)
        return 1
    print("wrote %d chars, %d words" % (len(TEXT), len(TEXT.split())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
