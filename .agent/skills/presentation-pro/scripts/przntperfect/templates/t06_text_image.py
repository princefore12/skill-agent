"""06 - Text + image placeholder, bottom-right (Figma node 562:214)."""

from .. import primitives as P
from ._common import white_bg, light_footer, placeholder, section_two_tone


def build(deck):
    s = deck.add_slide()
    white_bg(s)
    P.add_two_tone(s, 53, 50, 897, 215, section_two_tone(), size_px=64,
                   line_height_pct=100)
    placeholder(s, 663, 351, 1207, 679)
    light_footer(s)
    return s
