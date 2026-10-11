"""03 - Section statement on Semi-Light (Figma node 583:81).

Resolved VERIFY: on the Semi-Light background the three-line heading is MONOTONE
Graphite (#454E63) -- not a High/Gray-Dark two-tone. No footer on this slide.
"""

from .. import primitives as P
from ._common import SEMI_LIGHT, GRAPHITE, SECTION_TEXT


def build(deck):
    s = deck.add_slide()
    P.add_solid_background(s, SEMI_LIGHT)
    P.add_text(s, 50, 68, 1569, 210, SECTION_TEXT, size_px=64,
               line_height_pct=100, color=GRAPHITE)
    return s
