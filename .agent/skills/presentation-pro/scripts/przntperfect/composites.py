"""Higher-level composites built purely from primitives.

These cover the two templates that the client requires be reproduced with plain
shapes/text/lines rather than native chart or table objects (slides 14 and 15):
a bar chart and a pseudo-table. Nothing here creates a native PPT chart or table.
"""

from .primitives import add_rect, add_hairline, add_text
from .grid import GRID


# --------------------------------------------------------------------------- #
# bar chart (shapes only)
# --------------------------------------------------------------------------- #
def bar_chart_geometry(n, start_col=0, span_cols=None, gap_cols=0):
    """Grid-true bar x-positions and width for an ``n``-bar chart.

    Client rule (2026-08-05): a bar is always a whole number of grid columns wide
    and every bar sits on a column boundary — never the thin, off-grid bars the
    model used to draw. Bars are laid left to right ``span_cols`` columns apart
    (plus any ``gap_cols`` of empty column between them); adjacent bars are
    separated by the 20px gutter.

    Bar width AUTO-SCALES with the count (client rule 2026-08-06): with
    ``span_cols=None`` (the default) a bar is **two columns** wide for up to 6
    bars (6 two-col bars fill the full 12-column width), and drops to **one
    column** for 7-12 bars so the extra bars still fit the width. Pass an explicit
    ``span_cols`` to override. Returns ``(xs, width)``; raises if the bars overrun
    the 12-column grid.
    """
    if n < 1:
        raise ValueError("bar_chart_geometry: n must be >= 1")
    if span_cols is None:                       # auto: 2 cols/bar up to 6, else 1
        span_cols = 2 if n <= 6 else 1
    step = span_cols + gap_cols
    last_col = start_col + (n - 1) * step + (span_cols - 1)
    if last_col > GRID.t.col_count - 1:
        raise ValueError(
            f"bar_chart_geometry: {n} bars of {span_cols} cols "
            f"(step {step}) from col {start_col} overrun the "
            f"{GRID.t.col_count}-column grid")
    xs = [GRID.col_x(start_col + i * step) for i in range(n)]
    return xs, GRID.col_width(span_cols)


def add_bar(slide, x_px, top_px, w_px, baseline_px, rgb):
    """A single vertical bar: rectangle from ``top_px`` down to ``baseline_px``."""
    return add_rect(slide, x_px, top_px, w_px, baseline_px - top_px, rgb)


def add_bar_chart(
    slide, bars, baseline_y_px, baseline_color, baseline_weight_px=1,
    value_size_px=48, value_color=None, value_top_offset_px=18,
    value_inset_px=12, bar_bottom_px=None,
):
    """Draw an ascending bar chart from shapes only.

    ``bars`` is a list of dicts, each with:
        x, width, top   -- bar rectangle geometry (px)
        color           -- fill RGBColor
        value           -- optional value label string (e.g. '30x'); None = none
    A single baseline hairline spans from the first bar's left to the last bar's
    right, drawn at ``baseline_y_px``. Bar rectangles bottom out at
    ``bar_bottom_px`` when supplied (the Figma reference floats the bars a few px
    ABOVE the axis line); otherwise they sit directly on ``baseline_y_px``.
    Value labels sit just inside the top of their bar, left-aligned.
    """
    bottom = baseline_y_px if bar_bottom_px is None else bar_bottom_px
    for b in bars:
        add_bar(slide, b["x"], b["top"], b["width"], bottom, b["color"])

    left = min(b["x"] for b in bars)
    right = max(b["x"] + b["width"] for b in bars)
    add_hairline(slide, left, baseline_y_px, right - left, baseline_color,
                 weight_px=baseline_weight_px)

    for b in bars:
        if b.get("value"):
            add_text(
                slide, b["x"], b["top"] + value_top_offset_px, b["width"], 80,
                b["value"], size_px=value_size_px, line_height_pct=100,
                align="l", color=value_color, left_inset_px=value_inset_px,
            )


# --------------------------------------------------------------------------- #
# pseudo-table (text + hairlines)
# --------------------------------------------------------------------------- #
def add_pseudo_table(
    slide, rules, cells, cell_size_px=26, cell_color=None,
    cell_line_height_pct=124, rule_color=None, rule_weight_px=1,
    cell_width_px=340,
):
    """Draw a table entirely from hairlines and text.

    ``rules`` -- list of ``(y_px, x_start_px, width_px)`` horizontal hairlines.
    ``cells`` -- list of ``(x_px, y_px, text)`` left-aligned text cells; a cell
    may override style via a 4th/5th tuple element ``(x, y, text, size_px, rgb)``.
    """
    for y, x, w in rules:
        add_hairline(slide, x, y, w, rule_color, weight_px=rule_weight_px)

    for cell in cells:
        x, y, text = cell[0], cell[1], cell[2]
        size = cell[3] if len(cell) > 3 else cell_size_px
        rgb = cell[4] if len(cell) > 4 else cell_color
        add_text(
            slide, x, y, cell_width_px, 40, text, size_px=size,
            line_height_pct=cell_line_height_pct, align="l", color=rgb,
        )
