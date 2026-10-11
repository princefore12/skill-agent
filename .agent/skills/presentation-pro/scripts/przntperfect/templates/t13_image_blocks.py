"""13 - Image left + two captioned blocks (Figma node 562:317).

Two-tone H1 keeps the canonical Figma typo "Typografy". Right column has two
blocks, each an H4 label (Graphite) over a muted Gray-Dark body.
"""

from .. import primitives as P
from ._common import (
    white_bg, light_footer, placeholder, HIGH, GRAPHITE, GRAY_DARK,
)

# BODY_LONG at 26px within a 593px column wraps to these 8 lines in the reference.
# Breaks are pinned with explicit "\n" (the engine turns each into <a:br/>) so
# PowerPoint's line-breaker cannot re-flow the paragraph differently from Figma.
# Verified char-for-char: " ".join(lines) == _common.BODY_LONG.
BODY13 = "\n".join([
    "Built on advanced mathematics and signal science,",
    "our technology bridges the gap between theoretical",
    "models and physical reality. it captures patterns",
    "hidden deep within noise, revealing structure where",
    "others see randomness. this clarity unlocks new",
    "levels of control, accuracy, and insight across",
    "industries that depend on precision — from sensing",
    "and navigation to manufacturing and defense.",
])


def build(deck):
    s = deck.add_slide()
    white_bg(s)
    # Canonical typo "Typografy" preserved intentionally. Reference shows a
    # ~2-space gap before the accent run (measured 36px vs 22px for one space),
    # so the graphite run carries two trailing spaces.
    # y=54 (was 50): 64px cap lands box_top+4 under the exact-spcPts engine;
    # reference cap top measured y58 (render y54 at box 50). Widths match ref
    # (graphite 272/blue 283) so tracking stays on.
    P.add_two_tone(s, 50, 54, 900, 100,
                   [("Typografy  ", GRAPHITE), ("$25B TAM", HIGH)],
                   size_px=64, line_height_pct=100)
    placeholder(s, 50, 203, 1053, 827)

    # Block A. Labels are H3 (36px/110%), NOT H4 (32px): reference "Semiconductors"
    # measures 250px wide vs 221px rendered at 32px (ratio 1.13 -> 36px).
    P.add_text(s, 1277, 235, 593, 45, "Semiconductors", size_px=36,
               line_height_pct=110, color=GRAPHITE)
    # body y=299,x=1276 (were 298,1277): the body block was uniformly 1px above and
    # 1px right of the reference (measured line tops 305/306, left 1279/1277). A
    # (dy+1,dx-1) nudge cut the block's masked-diff ~67% (30.7k -> 10.0k px each) --
    # the dominant slide-13 win. Pitch already matches ref (34px). glyph gap 65px.
    P.add_text(s, 1276, 299, 593, 270, BODY13, size_px=26,
               line_height_pct=132, color=GRAY_DARK)
    # Block B
    P.add_text(s, 1277, 662, 593, 45, "12.43 msec", size_px=36,
               line_height_pct=110, color=GRAPHITE)
    # Same 1px-up/1px-right offset as block A (identical measured tops/lefts).
    P.add_text(s, 1276, 726, 593, 270, BODY13, size_px=26,
               line_height_pct=132, color=GRAY_DARK)
    light_footer(s)
    return s
