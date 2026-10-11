"""Sanctioned card-row component for the Prznt Perfect Slides engine.

The model kept re-inventing the "row of cards" pattern by hand and drifting off
the system -- rounded corners, drop shadows, text baked *inside* a filled shape,
eyebrow labels, and mismatched per-card padding. ``add_card_row`` is the one
blessed way to draw a row of cards so every card in the deck lands on the same
grid.

What a card IS (and is NOT)
---------------------------
* A card is a **flat, sharp-cornered, borderless, shadow-free** ``White-Cool``
  rectangle (built through :func:`primitives.add_rect`, which suppresses the
  inherited theme shadow). It carries **no text of its own** -- an OOXML shape
  with a fill *and* text inside it is exactly the "badge" anti-pattern the linter
  rejects.
* The card's content is a stack of **separate, transparent text boxes** drawn on
  top of the rectangle (through :func:`primitives.add_text`, so every run is
  Arial Regular with -1% tracking and exact ``spcPts`` line pitch).

Row geometry
------------
Cards are QUANTIZED TO GRID COLUMNS (client rule 2026-07-26): every card
spans a whole number of columns and every edge lands exactly on a column
guide; the gaps between cards are the 20px gutters themselves.

* **2 cards** -> 6 columns each: ``w = 900``,  ``x = 50 / 970``
* **3 cards** -> 4 columns each: ``w = 593.3``, ``x = 50 / 663.3 / 1276.7``
* **4 cards** -> 3 columns each: ``w = 440``,  ``x = 50 / 510 / 970 / 1430``

(The Figma slide-10 canon had cards at 438px / x514 — 2-4px OFF its own
grid; corrected to true column snapping per the client's grid principle.)

Stack geometry
--------------
Every card in the row shares the SAME internal padding and the SAME per-element
y-offsets, so the three stack slots line up across the whole row even when some
cards omit a field:

* slot 0 -- 48px (24pt) ``High`` number heading (a step number OR a stat value)
* slot 1 -- 36px (18pt) ``Graphite`` text heading (the card title)
* slot 2 -- 32px (16pt) ``Gray-Dark`` body / main text

(Card typography standard, client rule 2026-08-05 -- see the CARD_*_PX
constants below. The same three sizes apply to every component in
``components.py``.)

A missing field simply leaves its slot empty; the remaining elements do NOT move
up to fill the gap (that is the whole point -- a numbered card and an un-numbered
card in the same row keep their titles on one line).

One exception keeps the padding even: if NO card in the row uses slot 0
(number/value), the reserved top slot would leave the title at 120px while the
left inset is only 40px. The whole stack is then shifted up so the topmost used
slot lands on ``pad_px`` -- the top inset equals the left inset. (A row where at
least one card is numbered keeps the reserved slot, so cards still align.)

``cards`` API
-------------
``cards`` is a list of dicts, one per card, with any of these optional keys:

    ``number``  -> slot 0 text (e.g. ``"01"``)   -- 48px (24pt) High
    ``value``   -> slot 0 text (e.g. ``"$25B"``)  -- 48px (24pt) High
    ``title``   -> slot 1 text                    -- 36px (18pt) Graphite
    ``body``    -> slot 2 text                     -- 32px (16pt) Gray-Dark

``number`` and ``value`` share slot 0; if both are present ``number`` wins.

Examples (the three real cases seen in the wild)
------------------------------------------------
Problem cards -- title + body, no number::

    add_card_row(slide, [
        {"title": "Fragmented data", "body": "Signals scatter across silos."},
        {"title": "Slow response",   "body": "Insight arrives too late."},
        {"title": "Hidden risk",     "body": "Failures surface unseen."},
    ], y_px=300, h_px=560)

Stats -- value + title, no body::

    add_card_row(slide, [
        {"value": "$25B", "title": "Addressable market"},
        {"value": "30x",  "title": "Faster processing"},
        {"value": "0.18", "title": "msec latency"},
        {"value": "99.9%", "title": "Uptime"},
    ], y_px=340, h_px=360)

Numbered steps -- number + title + body::

    add_card_row(slide, [
        {"number": "01", "title": "Capture", "body": "Raw signals in."},
        {"number": "02", "title": "Model",   "body": "Structure from noise."},
        {"number": "03", "title": "Reveal",  "body": "Patterns made clear."},
    ], y_px=300, h_px=600)
"""

from .tokens import TOKENS
from .grid import GRID
from . import primitives as P

# --------------------------------------------------------------------------- #
# palette
# --------------------------------------------------------------------------- #
_WHITE_COOL = TOKENS.color("White-Cool")   # card fill  #EDEFF2
_HIGH = TOKENS.color("High")               # slot 0     #00A1FF
_GRAPHITE = TOKENS.color("Graphite")       # slot 1     #454E63
_GRAY_DARK = TOKENS.color("Gray-Dark")     # slot 2     #A8B1C7

# --------------------------------------------------------------------------- #
# row geometry (px on the 1920x1080 canvas)
# --------------------------------------------------------------------------- #
MARGIN_PX = TOKENS.margin_px               # 50
CONTENT_W_PX = TOKENS.content_w_px         # 1820
GAP_PX = 20                                # inter-card gap = the grid gutter
#: the bottom grid line (y=993.5) — cards sit their BOTTOM edge here by default.
GRID_BOTTOM_PX = TOKENS.margin_px + TOKENS.content_h_px

# --------------------------------------------------------------------------- #
# stack geometry (px, relative to each card's top-left) -- IDENTICAL per card
# --------------------------------------------------------------------------- #
PAD_PX = 40                                # left / right / top inner padding
NUM_DY_PX = 40                             # slot 0 (48px number) top offset
# The title sits DIRECTLY under the number — no gap between the two lines
# (client rule 2026-08-06): title_dy = num_dy + one number line (48px) = 88, so
# the number heading and the title read as two tight consecutive lines.
TITLE_DY_PX = 88                           # slot 1 (36px title)  top offset
BODY_DY_PX = 146                           # slot 2 (32px body)   top offset

# Slot box heights (top-anchored, transparent -- generous, do not affect layout).
_NUM_H_PX = 60
_TITLE_H_PX = 56

# --------------------------------------------------------------------------- #
# Card typography standard (client rule 2026-08-05) -- applies to EVERY card,
# here and in components.py. Given in PowerPoint POINTS; the engine works in px
# on the 1920 canvas where pt = px x 0.5, so px = pt x 2:
#   * text heading   -> 18pt = 36px
#   * body / main    -> 16pt = 32px
#   * number heading -> 24pt = 48px   (a heading that is a bare number, e.g. "01")
# --------------------------------------------------------------------------- #
CARD_TITLE_PX, CARD_TITLE_LH = 36, 110     # 18pt -- text heading
CARD_BODY_PX, CARD_BODY_LH = 32, 132       # 16pt -- body / main text
CARD_NUM_PX, CARD_NUM_LH = 48, 100         # 24pt -- number heading

# Internal aliases (slot sizes) point at the standard above.
_NUM_SIZE, _NUM_LH = CARD_NUM_PX, CARD_NUM_LH
_TITLE_SIZE, _TITLE_LH = CARD_TITLE_PX, CARD_TITLE_LH
_BODY_SIZE, _BODY_LH = CARD_BODY_PX, CARD_BODY_LH


def card_row_geometry(count, margin_px=MARGIN_PX, content_w_px=CONTENT_W_PX,
                      gap_px=GAP_PX):
    """Return ``(xs, w)`` for a row of ``count`` cards, snapped to the grid.

    When 12 is divisible by ``count`` (1/2/3/4/6/12 cards) every card spans
    exactly ``12/count`` columns: edges land ON the column guides and the
    gaps are the 20px gutters (2 -> w=900, 3 -> w=593.3, 4 -> w=440).
    Other counts (e.g. 5) cannot snap to a 12-column grid; they fall back
    to an equal split with a gutter-width gap.
    """
    if count < 1:
        raise ValueError("card_row_geometry: count must be >= 1")
    if 12 % count == 0:
        span = 12 // count
        xs = [GRID.col_x(i * span) for i in range(count)]
        w = GRID.col_right(0, span=span) - GRID.col_x(0)
        return xs, w
    w = (content_w_px - (count - 1) * gap_px) / count
    xs = [margin_px + i * (w + gap_px) for i in range(count)]
    return xs, w


def add_card_row(slide, cards, y_px=None, h_px=None, bottom_px=None,
                 xs=None, w_px=None, pad_px=PAD_PX, num_dy_px=NUM_DY_PX,
                 title_dy_px=TITLE_DY_PX, body_dy_px=BODY_DY_PX):
    """Draw a row of sanctioned cards and return the list of card rectangles.

    Parameters
    ----------
    slide : the python-pptx slide.
    cards : list of dicts -- see the module docstring (``number`` / ``value`` /
        ``title`` / ``body``, all optional). Length drives the row geometry.
    h_px : the card height (px, required), shared by every card.
    bottom_px, y_px : vertical placement. By DEFAULT (both omitted) the row
        bottom-anchors to the grid bottom line (``GRID_BOTTOM_PX`` = 993.5): the
        card's bottom edge sits on it and the top is ``bottom - h_px``. Pass
        ``bottom_px`` to anchor the bottom elsewhere, or ``y_px`` for an explicit
        top. Never centre a card row on the slide.
    xs, w_px : optional geometry override. When omitted they are derived from
        ``len(cards)`` via :func:`card_row_geometry`.
    pad_px, num_dy_px, title_dy_px, body_dy_px : the shared stack constants,
        applied identically to every card so slots stay aligned across the row.

    Every card is a flat White-Cool rectangle (sharp corners, no border, no
    shadow) with its text drawn as separate transparent boxes on top -- never
    text baked into the filled shape.
    """
    if h_px is None:
        raise ValueError("add_card_row: h_px (card height) is required")
    # Cards ALWAYS sit their BOTTOM edge on the bottom grid line (client rule
    # 2026-08-06) -- never centred on the slide. With no explicit top, the row
    # bottom-anchors to GRID_BOTTOM_PX (y=993.5). Pass bottom_px to anchor the
    # bottom elsewhere; pass y_px only for a deliberate top-based placement.
    if bottom_px is None and y_px is None:
        bottom_px = GRID_BOTTOM_PX
    if bottom_px is not None:
        y_px = bottom_px - h_px

    count = len(cards)
    if xs is None or w_px is None:
        gx, gw = card_row_geometry(count)
        xs = gx if xs is None else xs
        w_px = gw if w_px is None else w_px

    # Top inset must equal the left inset (pad_px): the topmost POPULATED slot
    # sits at pad_px. The fixed slot offsets reserve a number slot at the top so
    # numbered and un-numbered cards align across a MIXED row -- but when NO card
    # in the row carries a number/value, that reserved slot leaves an uneven top
    # gap (title at 120px against the 40px left inset). Collapse it: shift the
    # whole stack up so the first used slot lands on pad_px. Inter-slot gaps and
    # in-row alignment are preserved (every card shares the one shift).
    has_slot0 = any(c.get("number", c.get("value")) is not None for c in cards)
    has_slot1 = any(c.get("title") is not None for c in cards)
    first_dy = num_dy_px if has_slot0 else (title_dy_px if has_slot1 else body_dy_px)
    shift = first_dy - pad_px
    num_dy_px -= shift
    title_dy_px -= shift
    body_dy_px -= shift

    text_w = w_px - 2 * pad_px
    rects = []
    for card, x in zip(cards, xs):
        # 1) the card itself: flat, sharp, borderless, shadow-free rectangle.
        rect = P.add_rect(slide, x, y_px, w_px, h_px, _WHITE_COOL)
        rects.append(rect)

        tx = x + pad_px

        # 2) slot 0 -- Num-Head 48px High (number preferred, else value).
        slot0 = card.get("number", card.get("value"))
        if slot0 is not None:
            P.add_text(slide, tx, y_px + num_dy_px, text_w, _NUM_H_PX,
                       str(slot0), size_px=_NUM_SIZE, line_height_pct=_NUM_LH,
                       color=_HIGH)

        # 3) slot 1 -- H4 32px Graphite title.
        if card.get("title") is not None:
            P.add_text(slide, tx, y_px + title_dy_px, text_w, _TITLE_H_PX,
                       str(card["title"]), size_px=_TITLE_SIZE,
                       line_height_pct=_TITLE_LH, color=_GRAPHITE)

        # 4) slot 2 -- Body-Small 20px Gray-Dark body.
        if card.get("body") is not None:
            body_h = max(h_px - body_dy_px - pad_px, _BODY_SIZE)
            P.add_text(slide, tx, y_px + body_dy_px, text_w, body_h,
                       str(card["body"]), size_px=_BODY_SIZE,
                       line_height_pct=_BODY_LH, color=_GRAY_DARK)

    return rects
