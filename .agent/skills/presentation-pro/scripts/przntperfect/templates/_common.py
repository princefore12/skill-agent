"""Shared constants and small helpers for the 15 canonical template generators.

Palette shortcuts, the repeated section-statement copy, and DRY helpers for the
white background and the light-background footer. Colours reflect what the
reference PNGs actually render (see the build report / resolved VERIFY notes):
two-tone dark parts use Graphite (#454E63), muted parts use Gray-Dark (#A8B1C7),
accent uses High (#00A1FF).
"""

from ..tokens import TOKENS
from .. import primitives as P


def C(name):
    return TOKENS.color(name)


# palette shortcuts
HIGH = C("High")
HIGH1 = C("High-1")
HIGH2 = C("High-2")
HIGH3 = C("High-3")
HIGH4 = C("High-4")
GRAPHITE = C("Graphite")
GRAY_DARK = C("Gray-Dark")
GREY_LIGHT = C("Grey-Light")
WHITE_COOL = C("White-Cool")
SEMI_LIGHT = C("Semi-Light")
NAVY = C("Navy")
WHITE = C("White")
MAIN_NAVY = C("Main-Navy")
BLACK = C("Black")

CHART_SERIES = [C(n) for n in TOKENS.chart_series]  # High, High-1..4

# Repeated section-statement copy (verbatim from the reference renders).
SECTION_TEXT = "Seeing beyond\nsignals to reveal patterns\nhidden in plain sight"


def section_two_tone():
    """Two-tone section heading for white backgrounds: accent line + muted rest."""
    return [
        ("Seeing beyond", HIGH),
        ("\nsignals to reveal patterns\nhidden in plain sight", GRAY_DARK),
    ]


# Long body paragraph reused by slides 12 and 13.
BODY_LONG = (
    "Built on advanced mathematics and signal science, our technology bridges "
    "the gap between theoretical models and physical reality. it captures "
    "patterns hidden deep within noise, revealing structure where others see "
    "randomness. this clarity unlocks new levels of control, accuracy, and "
    "insight across industries that depend on precision — from sensing and "
    "navigation to manufacturing and defense."
)


def white_bg(slide):
    P.add_solid_background(slide, WHITE)


def light_footer(slide, page="10"):
    """Caption + pagination in Gray-Dark (slides 04, 06-15)."""
    P.add_footer(slide, caption_color=GRAY_DARK, page=page, page_color=GRAY_DARK)


def placeholder(slide, x, y, w, h):
    return P.add_image_placeholder(slide, x, y, w, h, WHITE_COOL)
