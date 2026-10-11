"""01 - Cover / closing (Figma node 670-1022, client redesign 2026-08-06).

Navy->blue vertical gradient background; a two-tone 110px (=55pt) H1 (High
accent + Gray-Dark muted); and the bottom-left date + quarter pills (Figma node
670-1017). The LAST slide of a deck reuses this same builder — see
``components.add_gradient_cover``.

Supersedes the earlier 72px Graphite-gradient cover.
"""

from .. import components as K
from ._common import HIGH, GRAY_DARK


def build(deck):
    s = deck.add_slide()
    K.add_gradient_cover(
        s,
        [("Seeing beyond", HIGH),
         ("\nsignals to reveal patterns\nhidden in plain sight", GRAY_DARK)],
        date="2026.11.12", quarter="Q4",
    )
    return s
