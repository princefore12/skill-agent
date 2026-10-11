"""08 - Text + image placeholder, top-right landscape (Figma node 583:105)."""

from .. import primitives as P
from ._common import white_bg, light_footer, placeholder, section_two_tone


def build(deck):
    s = deck.add_slide()
    white_bg(s)
    # Rule B: image at x970 = grid cols 7-12, so the text zone is cols 1-5 and
    # col 6 stays empty. Heading box width 746 (was 897) ends at ~799, clear of
    # col 6 (starts x816.7).
    P.add_two_tone(s, 53, 50, 746, 215, section_two_tone(), size_px=64,
                   line_height_pct=100)
    placeholder(s, 970, 50, 900, 483)
    light_footer(s)
    return s
