"""04 - Section statement on White (Figma node 562:148).

Resolved VERIFY: on White the heading IS two-tone -- accent line "Seeing beyond"
in High (#00A1FF), continuation in Gray-Dark (#A8B1C7). Footer present.
"""

from .. import primitives as P
from ._common import white_bg, light_footer, section_two_tone


def build(deck):
    s = deck.add_slide()
    white_bg(s)
    P.add_two_tone(s, 50, 56, 935, 252, section_two_tone(), size_px=64,
                   line_height_pct=100)
    light_footer(s)
    return s
