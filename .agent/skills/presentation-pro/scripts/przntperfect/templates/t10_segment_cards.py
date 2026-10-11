"""10 - Four segment cards (Figma node 562:3).

Two-tone H1 (Graphite + High); four H4 labels over four White-Cool cards.
The layout lists a 190x38 logo frame @(1672,50); the reference render shows that
area blank, so no visible logo shape is emitted.
"""

from .. import primitives as P
from ._common import white_bg, light_footer, placeholder, GRAPHITE, HIGH

LABELS = ["Automotive", "Aviation", "Defense", "Semiconductors"]
# Grid-snapped (client rule 2026-07-26): 4 cards x 3 columns, edges on the
# guides. Figma canon was 438px @ x514 -- 2-4px off its own grid; corrected.
XS = [50, 510, 970, 1430]


def build(deck):
    s = deck.add_slide()
    white_bg(s)
    P.add_two_tone(s, 50, 50, 900, 100,
                   [("Addresses ", GRAPHITE), ("$25B TAM", HIGH)],
                   size_px=64, line_height_pct=100)
    for x, label in zip(XS, LABELS):
        P.add_text(s, x, 463, 440, 45, label, size_px=32, line_height_pct=110,
                   color=GRAPHITE)
        placeholder(s, x, 509, 440, 483)
    light_footer(s)
    return s
