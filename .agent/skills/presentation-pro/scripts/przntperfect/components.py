"""Reusable, grid-snapped content components for the Prznt Perfect engine.

These are the card / subhead / annotation variants extracted from the client's
Figma "Cards" sheet (node 660:558, 2026-08-05). Every builder is placed by GRID
COLUMN, never raw pixels, so an element can only ever land on the 12-column grid
(client rule: "элементы встают всегда чётко по сетке"). Widths are fixed column
spans; heights and internal offsets reproduce the Figma geometry.

Placement
---------
Each builder takes ``col`` (0-based start column) and derives ``x = GRID.col_x``,
``w = GRID.col_width(span)``. Canonical row placements (edges land on guides,
gaps are the 20px gutters):

* span 6 (900px) — 2 per row at cols ``0, 6``         (bio / market cards)
* span 4 (593px) — 3 per row at cols ``0, 4, 8``      (metric card)
* span 3 (440px) — 4 per row at cols ``0, 3, 6, 9``   (problem / solution cards,
                                                        annotations)
* span 5 (747px) — right half at col ``7``            (numbered-steps table)

Component map (Figma name → builder)
------------------------------------
* Subhead                       → :func:`add_subhead`
* Card-1 / Card-1a  (bio)       → :func:`add_bio_card`
* Card-2            (market)    → :func:`add_market_card`
* Card-3            (problem)   → :func:`add_problem_card`
* Card-4            (solution)  → :func:`add_solution_card`
* Card-5 / Card-5a  (metric)    → :func:`add_metric_card`   (native table)
* Card2-Table-Numbers           → :func:`add_numbered_table` (native table)
* Annotation-1 / Annotation-2   → :func:`add_annotation`
* Bar-chart data table          → :func:`add_chart_data_table` (underline
                                  segmented to the bars, R14)
* Body paragraph group (1-2)    → :func:`add_paragraph_group` (tight stack,
                                  bottom-anchored to the grid, R16/R27)

All fill-bearing cards are flat, sharp-cornered White-Cool rectangles with their
text drawn as separate boxes on top (never text baked into a filled shape — the
linter's "badge" rule). Table cards are real ``GraphicFrame`` tables so rows stay
addable/editable. Subhead and card bodies are line-balanced (see textbalance).
"""

from .tokens import TOKENS
from .grid import GRID
from . import primitives as P
from math import ceil

from .tables import (stacked_rule_table, segmented_underline_table,
                     _disable_table_style, _fill_cell_paragraphs, _set_cell_box,
                     RULE_THIN, RULE_THICK, _GRAY_DARK_HEX)
from .textbalance import balance_lines, line_count, text_width_px
from .units import PXt
from .composites import bar_chart_geometry
from .cards import (CARD_TITLE_PX, CARD_TITLE_LH, CARD_BODY_PX, CARD_BODY_LH,
                    CARD_NUM_PX, CARD_NUM_LH, GRID_BOTTOM_PX)


def bottom_anchor(h_px, bottom_px=GRID_BOTTOM_PX):
    """Top y for a card of height ``h_px`` whose BOTTOM sits on the grid bottom.

    Cards always sit on the bottom grid line (y=993.5), never centred. For the
    component builders below (which take an explicit ``y_px``), pass
    ``y_px=bottom_anchor(h_px)``. ``add_card_row`` already bottom-anchors by
    default.
    """
    return bottom_px - h_px

# --------------------------------------------------------------------------- #
# palette + type scale (from the token source of truth)
# --------------------------------------------------------------------------- #
_WHITE_COOL = TOKENS.color("White-Cool")   # card fill        #EDEFF2
_HIGH = TOKENS.color("High")               # names / numbers  #00A1FF
_GRAPHITE = TOKENS.color("Graphite")       # titles / body    #454E63
_GRAY_DARK = TOKENS.color("Gray-Dark")     # muted / subtitle #A8B1C7
_GREY_LIGHT = TOKENS.color("Grey-Light")   # hairlines        #CCD1DB
_NAVY = TOKENS.color("Navy")               # dark section bg   #071A3C
_GREY_LIGHT_HEX = TOKENS.hex("Grey-Light").lstrip("#").upper()

#: Cover / closing gradient (Figma node 670-1022, pixel-sampled): a vertical
#: (top->bottom) ramp from Navy to a brighter blue. Quartile stops are pinned
#: because the renderer bows a two-stop ramp in a non-sRGB space (see primitives).
COVER_GRADIENT = [(0, "071A3C"), (25000, "051A3E"), (50000, "062248"),
                  (75000, "052D58"), (100000, "023A6C")]
#: Cover / closing title kegel (client rule 2026-08-06): 110px = 55pt (was 72).
COVER_TITLE_PX = 110
#: Cover / closing title letter spacing (client rule 2026-08-06): Condensed 1.5pt
#: (absolute, PowerPoint "Condensed by 1.5 points"), not the -1% used elsewhere.
COVER_TRACK_PT = -1.5

_H2, _H2_LH = TOKENS.size_px("H2"), TOKENS.line_height_pct("H2")            # 48/115
_H3, _H3_LH = TOKENS.size_px("H3"), TOKENS.line_height_pct("H3")            # 36/110
_BODY, _BODY_LH = TOKENS.size_px("Body"), TOKENS.line_height_pct("Body")    # 26/132
_BSM, _BSM_LH = TOKENS.size_px("Body-Small"), TOKENS.line_height_pct("Body-Small")  # 20/124
_NUM, _NUM_LH = TOKENS.size_px("Num-Head"), TOKENS.line_height_pct("Num-Head")      # 48/100

CARD_PAD = 64          # inner padding of every Figma card variant (not the 40 of cards.py)


def _place(col, span):
    """(x, w) in px for a component starting at grid column ``col`` spanning ``span``."""
    return GRID.col_x(col), GRID.col_width(span)


def _card_bg(slide, x, y, w, h):
    """Flat, sharp-cornered, shadow-free White-Cool card rectangle."""
    return P.add_rect(slide, x, y, w, h, _WHITE_COOL)


# --------------------------------------------------------------------------- #
# Subhead — the muted line(s) under the H1 title
# --------------------------------------------------------------------------- #
#: Subhead type: 12pt = 24px (client rule 2026-08-06).
SUBHEAD_PX, SUBHEAD_LH = 24, 124
#: Gap between the title text and the subhead (client rule 2026-08-06): 28px.
SUBHEAD_GAP_PX = 28
#: Arial cap-top sits ~0.0625*size below a text box top (pixel-measured: 4px at
#: 64px). Used to snap a title's capitals onto a grid line.
_CAP_TOP_FACTOR = 0.0625
#: Default title box top so its cap-top lands on the top margin line (y=50).
TITLE_BOX_Y = 46


def _cap_offset(size_px):
    return round(_CAP_TOP_FACTOR * size_px)


def _title_box_top(size_px, n_lines=1, cap_top_px=None):
    """Box top (px) so the first line's CAP-TOP lands on ``cap_top_px`` (default
    the top margin, y=50) -- the real "titles wander" fix (client 2026-08-06).

    With exact ``spcPts`` line spacing the first line's vertical position drifts
    two ways, both pixel-measured via fitz baselines across sizes 36-110:
      1. the cap-top sits ``0.0388*size + 1.27`` px below the box top (grows with
         size) -- so the old flat ``0.0625*size`` factor was right at 64px but
         ~3px off at 110px (the cover floated high);
      2. a MULTI-line block lifts its own first line ~2px higher than a
         single-line block of the same size -- so a wrapping title landed higher
         than a one-liner, which is the per-slide "wandering" the client saw.
    Correcting for both lands every title's caps on the grid line regardless of
    size or line count.
    """
    if cap_top_px is None:
        cap_top_px = TOKENS.margin_px
    off = 0.0388 * size_px + 1.27
    if n_lines >= 2:
        off -= 2.0
    return round(cap_top_px - off)


def _content_lines(content, width_px, size_px):
    """Rendered line count of a title (hard breaks + soft wrap at ``width_px``)."""
    full = content if isinstance(content, str) else "".join(t for t, _ in content)
    return sum(line_count(seg, width_px, size_px) for seg in full.split("\n")) or 1


def add_title(slide, content, size_px=64, line_height_pct=100, width_px=1500,
              x_px=50, cap_top_px=None, color=None):
    """Slide title with its CAP-TOP snapped onto a grid line (client rule
    2026-08-06).

    Fixes the "title floats above / doesn't reach the grid" inconsistency: the
    capital letters START exactly on the top margin line (y=50) on every slide,
    because the box top is offset by Arial's measured cap-top lead. ``content`` is
    a string or a list of ``(text, rgb)`` two-tone segments. Returns the number
    of lines the title occupies (pass it to :func:`add_subhead` as
    ``title_lines``). Widen/narrow ``width_px`` to control wrapping; a wrapping
    title still obeys the short-word rule (R33) via the engine's gluing.
    """
    # A monotone (plain-string) title defaults to Graphite so it matches the dark
    # part of every two-tone title (client fix 2026-08-06: the Agenda title was
    # rendering in the theme default, darker than other slides' Graphite titles).
    # Two-tone (list) content carries its own per-segment colors and is untouched.
    if color is None and isinstance(content, str):
        color = _GRAPHITE
    # Cap-top snaps onto the grid line regardless of size OR line count (R35): the
    # box top is offset by the calibrated first-line lead, which depends on both.
    nlines = _content_lines(content, width_px, size_px)
    y = _title_box_top(size_px, nlines, cap_top_px)
    # hug=True: the box shrinks to the title's measured bbox (R36) while the
    # top-left stays put, so the cap-top stays fixed on the grid line. (The new
    # hug sets the exact size up front instead of relying on auto-fit, so there is
    # no first-line sag — the reason the old code kept hug off.)
    P.add_text(slide, x_px, y, width_px, size_px * 3, content,
               size_px=size_px, line_height_pct=line_height_pct, color=color,
               hug=True)
    return nlines


def add_subhead(slide, subtitle, y_px=None, title_y_px=TITLE_BOX_Y, title_size_px=64,
                title_lines=1, gap_px=SUBHEAD_GAP_PX, x_px=50, cols=4,
                color=_GRAY_DARK, size_px=SUBHEAD_PX, line_height_pct=SUBHEAD_LH,
                balance=True):
    """Slide subhead: 12pt (24px) Gray-Dark, 10px below the title.

    Placed ``gap_px`` (10px) below the title text (from ``title_y_px`` 44 +
    ``title_size_px`` 64), capped at ``cols`` grid columns (4 max, R24), and
    line-balanced (R31): even line lengths, no widow/orphan, no article or 1-2
    letter word at a line end. If the title wraps, pass ``title_lines`` (2, 3…) so
    the subhead clears it. Pass an explicit ``y_px`` to override placement, or
    ``balance=False`` for a raw box.
    """
    if y_px is None:
        # Position so the VISUAL gap (title glyph bottom -> subhead glyph top) is
        # gap_px. Arial (pixel-measured): a title's glyphs bottom ~0.78*size below
        # its box top (no descender), and a box's first glyph top sits ~0.21*size
        # below its box top. For the standard 64px title + 24px subhead this puts
        # the subhead box at y~99 (10px visual gap). A multi-line title adds
        # (title_lines-1) full title lines first.
        y_px = round(title_y_px + (title_lines - 1) * title_size_px
                     + 0.78 * title_size_px + gap_px - 0.21 * size_px)
    cols = min(cols, 4)
    w = GRID.col_width(cols)
    text = balance_lines(subtitle, w, size_px) if balance else subtitle
    return P.add_text(slide, x_px, y_px, w, 200, text,
                      size_px=size_px, line_height_pct=line_height_pct, color=color)


# --------------------------------------------------------------------------- #
# Body paragraph group — 1-2 paragraphs as one bottom-anchored block
# --------------------------------------------------------------------------- #
def add_paragraph_group(slide, paragraphs, x_px=50, cols=4,
                        bottom_px=GRID_BOTTOM_PX, y_px=None, size_px=_BODY,
                        lh_pct=_BODY_LH, color=_GRAPHITE, spacing_px=None,
                        balance=True):
    """One or two body paragraphs as a single GROUP (client rule 2026-08-06).

    The paragraphs form ONE tight vertical stack and never drift apart: the gap
    between them is **two paragraph spacings** (``2 * spacing_px``, default 2x the
    font size). The whole group is treated as a unit and **bottom-anchored to the
    bottom grid line** (``bottom_px``, default 993.5) — its bottom edge sits on
    the grid line, like a card (R27). Each paragraph is line-balanced (R31).

    ``paragraphs`` is a string or a list of 1-2 strings. Width is ``cols`` grid
    columns (≤ 5, R17). Pass ``y_px`` to top-place the group instead of
    bottom-anchoring.
    """
    if isinstance(paragraphs, str):
        paragraphs = [paragraphs]
    w = GRID.col_width(min(cols, 5))
    spacing = size_px if spacing_px is None else spacing_px
    gap = 2 * spacing                              # two paragraph spacings
    pitch = size_px * lh_pct / 100.0

    texts = [balance_lines(p, w, size_px) if balance else p for p in paragraphs]
    heights = [(t.count("\n") + 1) * pitch for t in texts]
    total = sum(heights) + gap * (len(texts) - 1)

    # "Rests ON the line" (client choice 2026-08-06): the last line's LOWEST point
    # — the descender bottom of g/p/y — sits on the grid line, so the block stands
    # on it and NOTHING crosses below. Arial's descender bottom is ~1.15*size below
    # a line box top (pixel-measured: 30px at 26px); the last line box top is
    # (total - pitch) below the group top, so solve group top from that.
    descender_extent = 1.15 * size_px
    y = y_px if y_px is not None else (bottom_px - total + pitch - descender_extent)
    boxes = []
    for t, h in zip(texts, heights):
        # hug=False: the box is already tight (height = the wrapped text), and
        # auto-size would shift multi-line text (first-line sag), breaking the
        # descender-on-grid landing. Keep the fixed box so the anchor is exact.
        boxes.append(P.add_text(slide, x_px, round(y), w, round(h) + 2, t,
                                size_px=size_px, line_height_pct=lh_pct, color=color,
                                hug=False))
        y += h + gap
    return boxes


# --------------------------------------------------------------------------- #
# Card-1 / Card-1a — bio / person card (900 x 521)
# --------------------------------------------------------------------------- #
def add_bio_card(slide, col, y_px, name, role, bullets, span=6, h_px=521):
    """Bio card: name (H3 High) + role (Body-Small Gray-Dark) + a Body bullet list.

    (Figma Card-1 and Card-1a are the same component — "1a" is a duplicate.)
    ``bullets`` is a list of short single-line strings (Body 26px Graphite),
    stacked on a 46px pitch.
    """
    x, w = _place(col, span)
    _card_bg(slide, x, y_px, w, h_px)
    tx, tw = x + CARD_PAD, w - 2 * CARD_PAD

    P.add_text(slide, tx, y_px + 64, tw, 50, name,
               size_px=CARD_TITLE_PX, line_height_pct=CARD_TITLE_LH, color=_HIGH)
    if role:
        # Role (person's job title) is Graphite, not muted (client rule 2026-08-06).
        P.add_text(slide, tx, y_px + 110, tw, 30, role,
                   size_px=_BSM, line_height_pct=_BSM_LH, color=_GRAPHITE)
    for i, b in enumerate(bullets):
        P.add_text(slide, tx, y_px + 183 + i * 46, tw, 40, b,
                   size_px=CARD_BODY_PX, line_height_pct=CARD_BODY_LH, color=_GRAPHITE)
    return


# --------------------------------------------------------------------------- #
# Card-2 — market / region card (900 x 369)
# --------------------------------------------------------------------------- #
def add_market_card(slide, col, y_px, header, bullets, span=6, h_px=369):
    """Market card: a header (H3, may be two-tone) + a Body bullet list.

    ``header`` is a plain string (Graphite) or a list of ``(text, rgb)`` segments
    for a two-tone header (e.g. ``[("North America", GRAPHITE), (" – primary
    market", HIGH)]``). ``bullets`` is a list of short Body strings on a 46px pitch.
    """
    x, w = _place(col, span)
    _card_bg(slide, x, y_px, w, h_px)
    tx, tw = x + CARD_PAD, w - 2 * CARD_PAD

    color = None if isinstance(header, list) else _GRAPHITE
    P.add_text(slide, tx, y_px + 64, tw, 50, header,
               size_px=CARD_TITLE_PX, line_height_pct=CARD_TITLE_LH, color=color)
    for i, b in enumerate(bullets):
        P.add_text(slide, tx, y_px + 152 + i * 46, tw, 40, b,
                   size_px=CARD_BODY_PX, line_height_pct=CARD_BODY_LH, color=_GRAPHITE)
    return


# --------------------------------------------------------------------------- #
# Card-3 — problem card (440 x 445)
# --------------------------------------------------------------------------- #
def add_problem_card(slide, col, y_px, title, body, span=3, h_px=445,
                     body_color=_GRAY_DARK, balance=True):
    """Problem card: a big H2 title (up to 2 lines, Graphite) + a short Body note.

    The note is line-balanced by default.
    """
    x, w = _place(col, span)
    _card_bg(slide, x, y_px, w, h_px)
    tx, tw = x + CARD_PAD, w - 2 * CARD_PAD

    P.add_text(slide, tx, y_px + 64, tw, 120, title,
               size_px=CARD_TITLE_PX, line_height_pct=CARD_TITLE_LH, color=_GRAPHITE)
    if body:
        text = balance_lines(body, tw, CARD_BODY_PX) if balance else body
        P.add_text(slide, tx, y_px + 222, tw, 200, text,
                   size_px=CARD_BODY_PX, line_height_pct=CARD_BODY_LH, color=body_color)
    return


# --------------------------------------------------------------------------- #
# Card-4 — numbered solution card (440 x 445)
# --------------------------------------------------------------------------- #
def add_solution_card(slide, col, y_px, number, title, body, span=3, h_px=445,
                      body_color=_GRAY_DARK, balance=True):
    """Solution card: number (Num-Head High) + H2 title (Graphite) + Body note."""
    x, w = _place(col, span)
    _card_bg(slide, x, y_px, w, h_px)
    tx, tw = x + CARD_PAD, w - 2 * CARD_PAD

    # Number heading, then the title DIRECTLY under it — no gap (client rule
    # 2026-08-06): title at +64 + one number line (48px) = +112.
    P.add_text(slide, tx, y_px + 64, tw, 60, str(number),
               size_px=CARD_NUM_PX, line_height_pct=CARD_NUM_LH, color=_HIGH)
    P.add_text(slide, tx, y_px + 112, tw, 60, title,
               size_px=CARD_TITLE_PX, line_height_pct=CARD_TITLE_LH, color=_GRAPHITE)
    if body:
        text = balance_lines(body, tw, CARD_BODY_PX) if balance else body
        P.add_text(slide, tx, y_px + 215, tw, 200, text,
                   size_px=CARD_BODY_PX, line_height_pct=CARD_BODY_LH, color=body_color)
    return


# --------------------------------------------------------------------------- #
# Annotation-1 / Annotation-2 — top hairline + a muted note (440 x ~101)
# --------------------------------------------------------------------------- #
def add_annotation(slide, col, y_px, text, span=3, color=_GRAY_DARK,
                   size_px=_BSM, line_height_pct=_BSM_LH, rule_color=_GREY_LIGHT,
                   rule_weight_px=1, gap_px=25, balance=True):
    """Annotation: a top hairline with a Body-Small Gray-Dark note beneath it.

    Line-balanced. Used to caption a chart/card cluster to its side.
    """
    x, w = _place(col, span)
    P.add_hairline(slide, x, y_px, w, rule_color, weight_px=rule_weight_px)
    t = balance_lines(text, w, size_px) if balance else text
    return P.add_text(slide, x, y_px + gap_px, w, 200, t,
                      size_px=size_px, line_height_pct=line_height_pct, color=color)


# --------------------------------------------------------------------------- #
# Card2-Table-Numbers — numbered-steps NATIVE table (747 wide)
# --------------------------------------------------------------------------- #
def add_numbered_table(slide, col, y_px, steps, span=5, row_h_px=187.75):
    """Numbered steps as a real table: each row is a Num-Head number above Body
    text, separated by horizontal rules (top rule + a rule under every row).

    ``steps`` is a list of either plain strings (auto-numbered 1..N) or dicts
    ``{"number": .., "text": ..}``. Rows are addable/removable table rows.
    """
    x, w = _place(col, span)
    rows = []
    for i, s in enumerate(steps):
        if isinstance(s, dict):
            number, text = s.get("number", i + 1), s["text"]
        else:
            number, text = i + 1, s
        rows.append({
            "paras": [
                {"text": str(number), "size_px": CARD_NUM_PX, "color": _HIGH,
                 "lh_pct": CARD_NUM_LH},
                {"text": text, "size_px": CARD_BODY_PX, "color": _GRAPHITE,
                 "lh_pct": CARD_BODY_LH, "space_before_px": 12},
            ],
            "height_px": row_h_px,
            "bottom_rule": True,
        })
    return stacked_rule_table(slide, x, y_px, w, rows, rule_hex=_GREY_LIGHT_HEX,
                              top_rule=True, anchor="ctr")


# --------------------------------------------------------------------------- #
# Card-5 / Card-5a — metric NATIVE table on a White-Cool card (593 wide)
# --------------------------------------------------------------------------- #
def add_metric_card(slide, col, y_px, header, rows, span=4, h_px=599, card=True,
                    vpad_px=40, balance=True):
    """Metric card: a blue H3 headline over Body fact rows, separated by rules.

    ``header`` is the headline (H3 High); ``rows`` is a list of Body strings.
    Rows carry a bottom rule except the last. Built as a native table on a
    White-Cool card (``card=False`` omits the card fill — a bare table).
    ``h_px=None`` sizes the card to the table content.
    """
    x, w = _place(col, span)
    tx, tw = x + CARD_PAD, w - 2 * CARD_PAD

    entries = [(header, CARD_TITLE_PX, CARD_TITLE_LH, _HIGH)] + \
              [(t, CARD_BODY_PX, CARD_BODY_LH, _GRAPHITE) for t in rows]
    n = len(entries)
    trows = []
    for i, (txt, size, lh, color) in enumerate(entries):
        bt = balance_lines(txt, tw, size) if balance else txt
        nlines = bt.count("\n") + 1
        content = nlines * size * lh / 100.0
        first, last = (i == 0), (i == n - 1)
        marT = 0 if first else vpad_px
        height = marT + content + (0 if last else vpad_px)
        trows.append({
            "paras": [{"text": bt, "size_px": size, "color": color, "lh_pct": lh}],
            "height_px": height,
            "marT_px": marT,
            "bottom_rule": not last,
        })

    table_h = sum(r["height_px"] for r in trows)
    if card:
        card_h = (table_h + 2 * CARD_PAD) if h_px is None else h_px
        _card_bg(slide, x, y_px, w, card_h)
    return stacked_rule_table(slide, tx, y_px + CARD_PAD, tw, trows,
                              rule_hex=_GREY_LIGHT_HEX, top_rule=False, anchor="t")


# --------------------------------------------------------------------------- #
# Chart data table — underline SEGMENTED to the bars (R14)
# --------------------------------------------------------------------------- #
def add_chart_data_table(slide, rows, n=None, start_col=0, span_cols=None,
                         gap_cols=0, y_px=None, bottom_px=GRID_BOTTOM_PX,
                         row_h_px=80, size_px=26, lh_pct=124,
                         color=_GRAPHITE, rule_hex=None):
    """Data table that ALWAYS goes under a bar chart (R14), with each row's
    underline BROKEN to the bar widths — one segment under every bar, a gap over
    every inter-bar gutter (never one continuous rule).

    Columns align to the SAME bars as ``composites.bar_chart_geometry(n,
    start_col, span_cols, gap_cols)`` — pass the identical args you used to lay
    out the chart so the segments sit exactly under the bars.

    By DEFAULT the table is **bottom-anchored to the grid line** (``bottom_px``,
    993.5): its last row's bottom sits on it, so the table never runs past the
    baseline (R27). Pass ``y_px`` to top-place it instead.

    ``rows`` is a list of rows, each a list of ``n`` cell strings (one per
    bar/column); e.g. a header row of period labels then value rows. Short rows
    are padded with blanks. Default text is Table-Numbers 26px Graphite; the
    underline is 0.5pt Gray-Dark (the canonical chart-table rule).
    """
    if n is None:
        n = max(len(r) for r in rows)
    xs, bar_w = bar_chart_geometry(n, start_col, span_cols, gap_cols)
    content_widths = [bar_w] * n
    spacer_widths = [xs[i + 1] - (xs[i] + bar_w) for i in range(n - 1)]

    trows = []
    for cells in rows:
        specs = [{"text": str(c), "size_px": size_px, "color": color,
                  "lh_pct": lh_pct} for c in cells]
        while len(specs) < n:                       # pad short rows to n columns
            specs.append({"text": "", "size_px": size_px, "color": color,
                          "lh_pct": lh_pct})
        trows.append({"cells": specs, "height_px": row_h_px, "bottom_rule": True})

    if y_px is None:                                 # bottom-anchor to the grid line
        y_px = bottom_px - row_h_px * len(trows)
    kw = {} if rule_hex is None else {"rule_hex": rule_hex}
    return segmented_underline_table(slide, xs[0], y_px, content_widths,
                                     spacer_widths, trows, anchor="ctr", **kw)


def _balance_content(content, width_px, size_px, base_color, force_lines=None):
    """Balance a str or list of ``(text, color)`` segments to even lines (R31),
    optionally FORCING exactly ``force_lines`` lines, and return placement-ready
    content. ``balance_lines`` preserves character count, so for two-tone content
    the balanced text is redistributed across the original segment boundaries by
    char index (the accent phrase keeps its color; the line breaks fall right).
    To force N lines, a width of ~one line's worth is used so the greedy wrap
    yields N lines, which the balancer then evens out."""
    full = content if isinstance(content, str) else "".join(t for t, _ in content)
    w = width_px
    if force_lines and force_lines >= 2:
        w = text_width_px(full, size_px, tracking=False) / force_lines * 1.12
    balanced = balance_lines(full, w, size_px)
    if isinstance(content, str):
        return balanced
    if len(balanced) != len(full):                  # safety net: no char-index map
        balanced = full
    segs, pos = [], 0
    for t, c in content:
        segs.append((balanced[pos:pos + len(t)], base_color if c is None else c))
        pos += len(t)
    return segs


# --------------------------------------------------------------------------- #
# Section statement — big claim on a dark navy slide, two-tone (white + accent)
# --------------------------------------------------------------------------- #
def add_section_statement(slide, content, bg=None, base_color=None,
                          accent_color=None, width_px=1120, place_width_px=1600,
                          size_px=64, logo_name=None, logo_image=None):
    """A section / divider ("перебивочный") slide: a big claim on a dark navy
    background, TWO-TONE like every other slide's title — a white base plus a
    High accent phrase (client rule 2026-08-06: sections are no longer all-white).

    ``content`` is either:
      * a plain string -> placed all in ``base_color`` (white), balanced; or
      * a list of ``(text, color)`` segments -> two-tone. Use ``base_color``
        (white) for the plain parts and ``accent_color`` (High) for the accent
        phrase; a ``None`` segment color falls back to ``base_color``.

    The statement is the slide TITLE, so it lands at the same grid position as
    every title (cap-top on the top line, via :func:`add_title`), line-balanced
    to even lines. Returns the line count.
    """
    base_color = _WHITE_COOL if base_color is None else base_color
    accent_color = _HIGH if accent_color is None else accent_color
    P.add_solid_background(slide, _NAVY if bg is None else bg)

    placed = _balance_content(content, width_px, size_px, base_color)
    color = base_color if isinstance(placed, str) else None
    n = add_title(slide, placed, color=color,
                  width_px=place_width_px, size_px=size_px)
    if logo_name or logo_image:                  # brand mark top-right (dark bg)
        add_logo(slide, image_path=logo_image, name=logo_name, dark=True)
    return n


# --------------------------------------------------------------------------- #
# Cover / closing — gradient background, 110px title, date + quarter pills
# --------------------------------------------------------------------------- #
#: Date + quarter pill geometry (Figma node 670-1017), px on the 1920 canvas.
_PILL_X, _PILL_Y, _PILL_H = 51, 928, 103
_DATE_W, _QTR_W = 245, 105


def add_date_quarter(slide, date, quarter, x_px=_PILL_X, y_px=_PILL_Y,
                     text_color=None, line_color=None):
    """The bottom-left cover element (Figma node 670-1017): two adjacent pills —
    a wide DATE chip and a narrow QUARTER chip. Both the text AND the 1px outline
    are the High accent blue (client rule 2026-08-06), unfilled, 20px centered
    text (:func:`primitives.add_pill`). Use a dot/dash date format ("2026.11.12"),
    never slashes (a "n/m" string reads as pagination to the linter)."""
    text_color = _HIGH if text_color is None else text_color
    line_color = _HIGH if line_color is None else line_color
    P.add_pill(slide, x_px, y_px, _DATE_W, _PILL_H, str(date),
               text_color, line_color)
    P.add_pill(slide, x_px + _DATE_W, y_px, _QTR_W, _PILL_H, str(quarter),
               text_color, line_color)


def add_gradient_cover(slide, title, date=None, quarter=None, arrow=True,
                       lines=None, logo_name=None, logo_image=None,
                       title_y_px=None, title_x_px=50, size_px=COVER_TITLE_PX):
    """A cover / closing slide (client design 2026-08-06, Figma node 670-1022):
    the Navy->blue vertical gradient background, a big 110px (=55pt) two-tone
    title (High accent + Gray-Dark muted), the bottom-left date + quarter pills,
    and a bottom-right circular 'next' arrow. The last slide of a deck uses this
    same builder.

    ``title`` is a plain string (rendered in High) or a list of ``(text, color)``
    two-tone segments (accent High + muted Gray-Dark, like the reference). Its
    cap-top snaps ONTO the top grid line (y=50, R35) like every other title, and
    the box hugs the text (R36). The heading carries Condensed 1.5pt tracking
    (client rule 2026-08-06). Pass ``date``/``quarter`` for the pills (both in
    High now, e.g. "2026.11.12", "Q4"); ``arrow=False`` hides the arrow button.
    The CLOSING (back) cover uses ``arrow=False`` — the arrow is a cover-only
    affordance — and ``lines=2`` to force its phrase onto two balanced lines
    (client rule 2026-08-06). ``lines=N`` balances any cover title to N lines.
    """
    P.add_vertical_gradient_background(slide, COVER_GRADIENT)
    if lines:                                    # force the phrase onto N lines
        title = _balance_content(title, 1200, size_px, _GRAY_DARK, force_lines=lines)
    if title_y_px is None:                        # cap-top on the top grid line,
        nlines = _content_lines(title, 1820, size_px)   # corrected for line count
        title_y_px = _title_box_top(size_px, nlines)
    P.add_text(slide, title_x_px, title_y_px, 1820, size_px * 4, title,
               size_px=size_px, line_height_pct=100, align="l",
               color=_HIGH if isinstance(title, str) else None,
               track_pt=COVER_TRACK_PT, hug=True)
    if date is not None or quarter is not None:
        add_date_quarter(slide, "" if date is None else date,
                         "" if quarter is None else quarter)
    if arrow:                                    # circular arrow, bottom-right
        d = 105
        P.add_arrow_button(slide, 1870 - d, _PILL_Y - 1, d, _HIGH)
    if logo_name or logo_image:                  # brand mark top-right (dark bg)
        add_logo(slide, image_path=logo_image, name=logo_name, dark=True)
    return slide


# --------------------------------------------------------------------------- #
# Logo / company name — top-right brand mark (Figma node 674-1100)
# --------------------------------------------------------------------------- #
#: Top-right logo zone — HALF the original Figma 287x76 (client rule 2026-08-07):
#: the logo fits to height, so a logo image now stands 38px (=19pt) tall.
LOGO_W_PX, LOGO_H_PX = 143.5, 38
#: Company-name fallback size when there is NO logo image: 10pt = 20px (client
#: rule 2026-08-07). px = pt x 2 on the 1920 canvas, so 10pt -> 20px.
LOGO_NAME_PX = 20


def add_logo(slide, image_path=None, name=None, dark=False,
             right_px=None, top_px=None):
    """The top-right brand mark (Figma node 674-1100). Pass ``image_path`` for the
    user's LOGO — fit within a 287x76 zone, RIGHT+TOP aligned to the grid corner
    (the one sanctioned raster: a brand asset, not a content image). Or pass
    ``name`` for a text wordmark when they have no logo — right-aligned to the
    right margin (x=1870), cap-top on the top grid line (y=50). ``dark=True``
    renders the name in White-Cool for a dark section. A full-height image may
    cover it, which is fine (client rule 2026-08-06)."""
    right = (TOKENS.margin_px + TOKENS.content_w_px) if right_px is None else right_px
    top = TOKENS.margin_px if top_px is None else top_px
    if image_path:
        return P.add_picture(slide, image_path, right - LOGO_W_PX, top,
                             LOGO_W_PX, LOGO_H_PX, align="r", valign="t")
    if name:
        color = _WHITE_COOL if dark else _GRAPHITE
        w = ceil(text_width_px(name, LOGO_NAME_PX)) + 4
        y = _title_box_top(LOGO_NAME_PX, 1, top)      # cap-top on the top line
        return P.add_text(slide, right - w, y, w, LOGO_NAME_PX * 2, name,
                          size_px=LOGO_NAME_PX, line_height_pct=110, align="l",
                          color=color, hug=False)
    return None


# --------------------------------------------------------------------------- #
# Data table — native template-15 table placeable at ANY grid columns
# --------------------------------------------------------------------------- #
def add_data_table(slide, headers, rows, start_col=0, span_cols=12, y_px=None,
                   bottom_px=GRID_BOTTOM_PX, row_h_px=100, header_size=32,
                   cell_size=26, col_widths=None, color=None, rule_hex=None):
    """A native data table (template-15 look) placeable at ANY grid columns: a
    header row (heavier 1.5pt underline) over data rows (0.5pt underlines), all
    Gray-Dark, cells vertically centered, no verticals/fills. ``headers`` is the
    column labels; ``rows`` is a list of value-lists (short rows padded). Bottom-
    anchors to the grid line by default; equal column widths across the span
    unless ``col_widths`` (px) is given."""
    color = _GRAPHITE if color is None else color
    rhex = _GRAY_DARK_HEX if rule_hex is None else rule_hex
    x, w = GRID.col_x(start_col), GRID.col_width(span_cols)
    n = len(headers)
    col_widths = [w / n] * n if col_widths is None else col_widths
    nrows = 1 + len(rows)
    total_h = row_h_px * nrows
    if y_px is None:
        y_px = bottom_px - total_h
    gf = slide.shapes.add_table(nrows, n, PXt(x), PXt(y_px), PXt(w), PXt(total_h))
    t = gf.table
    _disable_table_style(t)
    for c in range(n):
        t.columns[c].width = PXt(col_widths[c])
    for c in range(n):                                # header row (thick underline)
        cell = t.cell(0, c)
        _fill_cell_paragraphs(cell, [{"text": str(headers[c]), "size_px": header_size,
                                      "color": color, "lh_pct": 110}])
        _set_cell_box(cell, 0, 0, 0, RULE_THICK, rhex, "ctr")
    for r, vals in enumerate(rows, start=1):          # data rows (thin underline)
        for c in range(n):
            v = str(vals[c]) if c < len(vals) else ""
            cell = t.cell(r, c)
            _fill_cell_paragraphs(cell, [{"text": v, "size_px": cell_size,
                                          "color": color, "lh_pct": 124}])
            _set_cell_box(cell, 0, 0, 0, RULE_THIN, rhex, "ctr")
    for r in range(nrows):
        t.rows[r].height = PXt(row_h_px)
    return gf


def add_side_table(slide, headers, rows, heading, body, side="left",
                   text_cols=3, table_cols=8, bottom_px=GRID_BOTTOM_PX,
                   row_h_px=100):
    """A NOT-full-width data table (Figma node 674-1028): an 8-column data table
    on one side and a 3-column text block (H3 heading + Body) on the other, with
    ONE empty grid column between them (client rule 2026-08-06). ``side`` is where
    the TEXT sits: "left" -> text cols 0..2 + gap col 3 + table cols 4..11;
    "right" -> table cols 0..7 + gap col 8 + text cols 9..11. Both bottom-anchor to
    the grid line so their bottoms align."""
    if side == "left":
        text_col, table_col = 0, text_cols + 1
    else:
        table_col, text_col = 0, table_cols + 1
    gf = add_data_table(slide, headers, rows, start_col=table_col,
                        span_cols=table_cols, bottom_px=bottom_px, row_h_px=row_h_px)
    # text block (H3 heading + Body), bottom-anchored to align with the table
    tx, tw = GRID.col_x(text_col), GRID.col_width(text_cols)
    body_bal = balance_lines(body, tw, _BODY)
    body_pitch = _BODY * _BODY_LH / 100.0
    head_pitch = _H3 * _H3_LH / 100.0
    gap = 24
    body_h = (body_bal.count("\n") + 1) * body_pitch
    top = bottom_px - (head_pitch + gap + body_h)
    P.add_text(slide, tx, round(top), tw, round(head_pitch) + 4, heading,
               size_px=_H3, line_height_pct=_H3_LH, color=_GRAPHITE)
    P.add_text(slide, tx, round(top + head_pitch + gap), tw, round(body_h) + 4,
               body_bal, size_px=_BODY, line_height_pct=_BODY_LH,
               color=_GRAY_DARK, hug=False)
    return gf
