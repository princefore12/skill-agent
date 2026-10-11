"""12-column / 26-row layout grid helper (all values in px on the 1920x1080 canvas).

Column and row sizes are the COMPUTED values (see tokens.py): Rules06 prints
135 px / 23 px, but those do not close against the 1820x980 content area, so the
engine computes col_width = (1820 - 11*20)/12 = 133.33 and
row_height = (980 - 25*14)/26 = 24.23.

Canonical templates use measured coordinates; this grid is for composing NEW
layouts on the same system.
"""

from .tokens import TOKENS


class Grid:
    def __init__(self, tokens=TOKENS):
        self.t = tokens

    # ---- columns ----
    def col_x(self, index):
        """Left x (px) of column ``index`` (0-based)."""
        t = self.t
        return t.margin_px + index * (t.col_width_px + t.col_gutter_px)

    def col_width(self, span=1):
        """Width (px) spanning ``span`` columns including inner gutters."""
        t = self.t
        return span * t.col_width_px + (span - 1) * t.col_gutter_px

    def col_right(self, index, span=1):
        return self.col_x(index) + self.col_width(span)

    # ---- rows ----
    def row_y(self, index):
        """Top y (px) of row ``index`` (0-based)."""
        t = self.t
        return t.margin_px + index * (t.row_height_px + t.row_gutter_px)

    def row_height(self, span=1):
        t = self.t
        return span * t.row_height_px + (span - 1) * t.row_gutter_px

    def row_bottom(self, index, span=1):
        return self.row_y(index) + self.row_height(span)

    # ---- convenience ----
    def cell(self, col, row, col_span=1, row_span=1):
        """Return (x, y, w, h) in px for a grid cell block."""
        return (
            self.col_x(col),
            self.row_y(row),
            self.col_width(col_span),
            self.row_height(row_span),
        )


GRID = Grid()
