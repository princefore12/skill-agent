"""09 - Text (vertically centred, left) + full-height image (Figma node 583:142)."""

from .. import primitives as P
from ._common import white_bg, light_footer, placeholder, HIGH, GRAY_DARK

# Rule B: image at x817 = grid cols 6-12, so the text zone is cols 1-4 and col 5
# stays empty; the heading box narrows to 593 (was 700), ending at ~646 (col 5
# starts x663.3). At H1 64px the shared section statement no longer fits 593px in
# <=3 lines ("signals to reveal patterns" alone is 699px), so this slide carries a
# shorter sentence-case (R1) two-tone variant preserving the "seeing beyond
# signals to reveal hidden patterns" meaning. Widest line 454px.
HEADING = [
    ("Seeing beyond", HIGH),
    ("\nsignals to reveal\nhidden patterns", GRAY_DARK),
]


def build(deck):
    s = deck.add_slide()
    white_bg(s)
    # Heading is vertically centred on the left column at y432 (measured).
    P.add_two_tone(s, 53, 432, 593, 215, HEADING, size_px=64,
                   line_height_pct=100)
    placeholder(s, 817, 50, 1053, 980)
    light_footer(s)
    return s
