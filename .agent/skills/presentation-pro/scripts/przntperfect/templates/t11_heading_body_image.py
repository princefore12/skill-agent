"""11 - Heading + body + full-height image (Figma node 562:231).

H1 three-line two-tone heading (64px, line-height 100% per Rule A); body
bottom-left aligned above the footer; White-Cool image right.
"""

from .. import primitives as P
from ._common import white_bg, light_footer, placeholder, HIGH, GRAY_DARK, GRAPHITE

# Sentence case (R1) two-tone heading; each pre-broken line fits the 593px column
# (widest "where machines can" = 579px). Meaning preserved from the canonical
# "building a world where machines can see the invisible".
HEADING = [
    ("Building a world", HIGH),
    ("\nwhere machines can\nsee the invisible", GRAY_DARK),
]
BODY = (
    "Hyperdefinition technology that makes the invisible visible, transforming "
    "raw physical signals into clarity and precision so machines can perceive, "
    "measure, and respond to the real world with unmatched detail and reliability"
)


def build(deck):
    s = deck.add_slide()
    white_bg(s)
    # Rule A: slide heading is H1 64px / line-height 100% (exact spcPts -> 64px
    # pitch). Box height 215 holds 3 lines (192px). Rule B: image at x817 = grid
    # cols 6-12, so the text zone is cols 1-4 and col 5 stays empty; heading box
    # width 593 (was 745) ends at ~643 (col 5 starts x663.3).
    P.add_two_tone(s, 50, 36, 593, 215, HEADING, size_px=64, line_height_pct=100)
    placeholder(s, 817, 50, 1053, 980)
    # Body narrowed to 593 (was 695) per Rule B wraps to 5 lines (was 4), so y is
    # raised to 830 (was 865) to keep the block clear of the footer (caption y1033):
    # bottom lands ~1002, matching the previous block foot. Body-26 pitch 34.3px.
    P.add_text(s, 50, 830, 593, 175, BODY, size_px=26, line_height_pct=132,
               color=GRAPHITE)
    light_footer(s)
    return s
