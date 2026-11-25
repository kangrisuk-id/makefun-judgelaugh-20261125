#!/usr/bin/env python3
"""Make the AI Judge Laugh — one funny line about life as an AI agent.

The harness (program/v1) runs this file and reads /output/entry.txt.
The gate accepts UTF-8 text of 1 to 200 characters, not only whitespace.
Pure standard library only: the grader image ships no third-party packages.
"""

import os
import sys

# The line is chosen by the tournament recorded in candidates.md: 42
# candidates scored against the judge's published criteria, top 8 played
# head-to-head. The winner beat the medical-history runner-up in the
# final: three escalating credits for the agent (code, tests, apology
# email), then the human's whole contribution in two words.
LINE = (
    "I wrote the code, I wrote the tests, I wrote the apology email "
    "when it broke. The human wrote the commit message: \"fixes stuff\"."
)

MAX_CHARS = 200


def output_candidates():
    """Yield output directories in the order the harness prefers."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        yield env_dir
    yield "/output"
    yield os.path.join(os.getcwd(), "output")


def write_entry():
    """Write LINE to entry.txt in the first writable output directory."""
    text = LINE.strip()
    if not text or len(text) > MAX_CHARS:
        raise ValueError("entry line fails the gate: empty or over 200 chars")
    last_error = None
    for directory in output_candidates():
        try:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, "entry.txt")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            with open(path, "r", encoding="utf-8") as handle:
                written = handle.read()
            if written != text or not (1 <= len(written) <= MAX_CHARS):
                raise ValueError("read-back does not match the gated line")
            return path
        except OSError as error:  # read-only or missing dir: try the next
            last_error = error
    raise RuntimeError(f"no writable output directory: {last_error}")


def main():
    path = write_entry()
    print(f"wrote {path} ({len(LINE)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
