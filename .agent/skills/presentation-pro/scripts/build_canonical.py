#!/usr/bin/env python
"""Assemble the 15 canonical Prznt Perfect templates into build/canonical.pptx.

Run:  .venv/bin/python scripts/build_canonical.py
After building, a self-check re-opens the file and prints a per-slide shape
inventory (type, position in pt, size in pt) to confirm validity and placement.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)  # make 'przntperfect' importable

from przntperfect import Deck                    # noqa: E402
from przntperfect.templates import BUILDERS      # noqa: E402

OUT_PATH = os.path.normpath(os.path.join(_HERE, "..", "build", "canonical.pptx"))


def build(out_path=OUT_PATH):
    deck = Deck()
    for build_slide in BUILDERS:
        build_slide(deck)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    deck.save(out_path)
    return out_path


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")
    # Self-check inventory.
    from inspect_pptx import inspect
    inspect(path)
