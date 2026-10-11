"""12 - Heading + two body blocks + full-height image (Figma node 562:202)."""

from .. import primitives as P
from ._common import (
    white_bg, light_footer, placeholder, HIGH, GRAY_DARK, GRAPHITE,
)

# Sentence case (R1) two-tone heading; each pre-broken line fits the 593px column
# (widest "where machines can" = 579px). Meaning preserved from the canonical
# "building a world where machines can see the invisible".
HEADING = [
    ("Building a world", HIGH),
    ("\nwhere machines can\nsee the invisible", GRAY_DARK),
]
# BODY_LONG at 20px within a 593px column wraps to these 7 lines in the reference
# (one fewer line than slide 13's 26px rendering of the same text). Breaks are
# pinned with explicit "\n" (engine -> <a:br/>) so the paragraph cannot re-flow.
# Verified char-for-char: " ".join(lines) == _common.BODY_LONG.
BODY1 = "\n".join([
    "Built on advanced mathematics and signal science, our technology",
    "bridges the gap between theoretical models and physical reality. it",
    "captures patterns hidden deep within noise, revealing structure",
    "where others see randomness. this clarity unlocks new levels of",
    "control, accuracy, and insight across industries that depend on",
    "precision — from sensing and navigation to manufacturing and",
    "defense.",
])
# BODY2 wraps to 5 reference lines; likewise pinned. " ".join == the flat source.
BODY2 = "\n".join([
    "Our technology, based on advanced math and signal science,",
    "connects theory with reality. It finds hidden patterns in noise,",
    "revealing structure where others see randomness. This clarity",
    "enables greater control, accuracy, and insight in industries needing",
    "precision—like sensing, navigation, manufacturing, and defense.",
])


def build(deck):
    s = deck.add_slide()
    white_bg(s)
    # Rule A: slide heading is H1 64px / line-height 100% (exact spcPts -> 64px
    # pitch). Box height 215 holds 3 lines (192px). Rule B: image at x817 = grid
    # cols 6-12, so the text zone is cols 1-4 and col 5 stays empty; heading box
    # width 593 (was 745) ends at ~643 (col 5 starts x663.3).
    P.add_two_tone(s, 50, 40, 593, 215, HEADING, size_px=64, line_height_pct=100)
    placeholder(s, 817, 50, 1053, 980)
    # Two paragraphs kept as separate boxes (Swiss blank-line separation, R2).
    # Reference renders these bodies as Body-Small (20px / 124%), NOT Body
    # (26px/132%): measured glyph width ratio 0.77 vs the 26px bodies on slide
    # 13, and 7-line wrap of BODY_LONG (vs 8 lines at 26px). See tokens
    # typography/styles/Body-Small.
    # lh 125: reference body pitch is exactly 25.0px/line (=20*1.25). BUT PowerPoint
    # rounds "Exactly" line spacing to whole points before rendering, so the 12.5pt
    # spcPts renders at round(12.5)*2 = 26px/line, not 25 -- an even-px quantum that
    # makes 25px unreachable (24 or 26 only). At 26px the block drifts +1px/line and
    # sagged ~+7px by line 7 with the box anchored at line 1. The y is therefore set
    # to CENTRE the residual drift about the block's middle line (measured optimum
    # dy-3/dy-4), roughly halving the vertical mismatch; x nudged +2/+1 to the
    # reference left edge. Residual is the pitch quantum (per-line boxes would remove
    # it entirely but are out of scope this round).
    P.add_text(s, 52, 665, 593, 190, BODY1, size_px=20, line_height_pct=125,
               color=GRAPHITE)
    P.add_text(s, 51, 864, 593, 150, BODY2, size_px=20, line_height_pct=125,
               color=GRAPHITE)
    light_footer(s)
    return s
