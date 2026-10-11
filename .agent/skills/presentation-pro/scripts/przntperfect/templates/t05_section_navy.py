"""05 - Section statement on Navy (Figma node 562:167).

Resolved VERIFY: on the Navy background the three-line heading is MONOTONE
White-Cool (#EDEFF2). No footer on this slide (reference shows none).
"""

from .. import primitives as P
from ._common import NAVY, WHITE_COOL, SECTION_TEXT


def build(deck):
    s = deck.add_slide()
    P.add_solid_background(s, NAVY)
    P.add_text(s, 50, 68, 1200, 210, SECTION_TEXT, size_px=64,
               line_height_pct=100, color=WHITE_COOL)
    return s
