"""Unit conversion for the Prznt Perfect Slides engine.

The reference designs are authored on a 1920x1080 px canvas. The output deck is
the standard PowerPoint 16:9 widescreen slide (13.333 x 7.5 in = 960 x 540 pt =
12192000 x 6858000 EMU).

px -> pt factor
---------------
`design-tokens.json` declares ``px_to_pt = 0.75`` (the 96-dpi convention, where
1 px = 0.75 pt). That factor maps 1920x1080 px onto 20 x 11.25 in, NOT onto the
13.333 x 7.5 in canvas the same file also declares (and that the build spec
requires). The two token values are mutually inconsistent.

To keep every 1920-px coordinate landing correctly on the required standard
slide, the engine DERIVES the factor from the target canvas geometry:

    PX_TO_PT = slide_pt_width / canvas_px_width = 960 / 1920 = 0.5

The tracking rule (-1% of the point size) is unaffected by this choice; only the
absolute point values change. See the build report for the full discrepancy note.
"""

from pptx.util import Pt, Emu

# Reference canvas (px) and target slide (pt) -- standard PowerPoint 16:9.
CANVAS_PX_WIDTH = 1920
CANVAS_PX_HEIGHT = 1080
SLIDE_PT_WIDTH = 960.0   # 13.3333 in
SLIDE_PT_HEIGHT = 540.0  # 7.5 in

# Derived, geometrically-consistent conversion factor (see module docstring).
PX_TO_PT = SLIDE_PT_WIDTH / CANVAS_PX_WIDTH  # == 0.5


def px_to_pt(px):
    """Convert a pixel length (float/int) to a point value (float)."""
    return px * PX_TO_PT


def PXt(px):
    """Convert a pixel length to a python-pptx ``Pt`` Length object."""
    return Pt(px * PX_TO_PT)


def tracking_spc(size_px):
    """DrawingML rPr@spc value (1/100 pt units) for -1% letter-spacing.

    spc = -round(size_pt), i.e. -1% of the point size expressed in 1/100 pt.
    Example: 26 px -> 13 pt -> spc = -13 (== -0.13 pt == -1% of 13 pt).
    """
    return -int(round(size_px * PX_TO_PT))
