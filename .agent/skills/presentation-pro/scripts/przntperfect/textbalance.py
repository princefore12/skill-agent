"""Balanced line wrapping for Prznt Perfect paragraphs.

PowerPoint (like Figma) greedily fills each line to the box width, which often
leaves the last line with a single orphaned word — "a long first line, then one
word below". The client wants *balanced* wrapping: the lines of a short paragraph
(a slide subhead, a card body) should come out roughly equal in length.

Approach
--------
1. Measure each word's rendered width in Arial Regular with the system's −1%
   tracking, using a static advance-width table (``_ARIAL_1000``, glyph advances
   per 1000 em, generated once from the system Arial.ttf — no runtime font
   dependency).
2. Greedily wrap at the full box width to learn the MINIMUM number of lines the
   text needs (``L``).
3. Binary-search the smallest line width ``W'`` that still wraps into ``≤ L``
   lines, then greedy-wrap at ``W'``. Minimizing the longest line for a fixed
   line count spreads the words evenly — that is the balance — while never
   adding an extra line or exceeding the box.

The result is the same text with explicit ``"\n"`` breaks inserted, ready to
hand to :func:`primitives.add_text` (which turns each ``"\n"`` into an ``<a:br/>``).
Callers that only want a width measurement can use :func:`text_width_px`.
"""

# Arial Regular advance widths, 1000 units/em, ASCII 32..126 (generated from
# /System/Library/Fonts/Supplemental/Arial.ttf; these are the standard Arial/
# Helvetica AFM advances, identical across platforms).
_ARIAL_1000 = {
    32: 278, 33: 278, 34: 355, 35: 556, 36: 556, 37: 889, 38: 667, 39: 191,
    40: 333, 41: 333, 42: 389, 43: 584, 44: 278, 45: 333, 46: 278, 47: 278,
    48: 556, 49: 556, 50: 556, 51: 556, 52: 556, 53: 556, 54: 556, 55: 556,
    56: 556, 57: 556, 58: 278, 59: 278, 60: 584, 61: 584, 62: 584, 63: 556,
    64: 1015, 65: 667, 66: 667, 67: 722, 68: 722, 69: 667, 70: 611, 71: 778,
    72: 722, 73: 278, 74: 500, 75: 667, 76: 556, 77: 833, 78: 722, 79: 778,
    80: 667, 81: 778, 82: 722, 83: 667, 84: 611, 85: 722, 86: 667, 87: 944,
    88: 667, 89: 667, 90: 611, 91: 278, 92: 278, 93: 278, 94: 469, 95: 556,
    96: 333, 97: 556, 98: 556, 99: 500, 100: 556, 101: 556, 102: 278, 103: 556,
    104: 556, 105: 222, 106: 222, 107: 500, 108: 222, 109: 833, 110: 556,
    111: 556, 112: 556, 113: 556, 114: 333, 115: 500, 116: 278, 117: 556,
    118: 500, 119: 722, 120: 500, 121: 500, 122: 500, 123: 334, 124: 260,
    125: 334, 126: 584,
}
# Fallback advance for any glyph outside the table (em-dash, accented letters,
# CJK, …): the em-dash-ish 1000, capped to a plausible average so exotic runs
# never wildly mis-measure. 600/1000 em is a safe Latin average.
_FALLBACK_1000 = 600


def char_advance_px(ch, size_px, tracking=True):
    """Rendered advance of one character in Arial Regular at ``size_px``.

    Includes the −1% tracking the system applies to every run (spc = −1% of the
    point size, i.e. −0.01·size_px added to each character's advance).
    """
    cp = 32 if ord(ch) == 0xA0 else ord(ch)   # NBSP advances like a normal space
    base = _ARIAL_1000.get(cp, _FALLBACK_1000) * size_px / 1000.0
    if tracking:
        base -= 0.01 * size_px
    return base


def text_width_px(text, size_px, tracking=True):
    """Rendered width (px) of a single-line string in Arial Regular at ``size_px``."""
    return sum(char_advance_px(c, size_px, tracking) for c in text)


# --------------------------------------------------------------------------- #
# typographic normalization (client rules 2026-08-06)
# --------------------------------------------------------------------------- #
_EM_DASH, _EN_DASH, _NBSP = "—", "–", " "
#: words that must never end a line — glued to the following word with an NBSP.
_ARTICLES = {"a", "an", "the"}


def normalize_dashes(text):
    """Em-dash -> en-dash: the system uses the en-dash only (never the em-dash)."""
    return text.replace(_EM_DASH, _EN_DASH)


def _is_glue(word):
    """True if ``word`` must not sit at a line end: an article or a 1-2 letter
    word (preposition/conjunction like 'of', 'to', 'in', 'is'). Pure punctuation
    (e.g. a spaced en-dash) is NOT a word and never glues."""
    w = "".join(c for c in word.lower() if c.isalnum())
    if not w:
        return False
    return w in _ARTICLES or len(w) <= 2


def _tokenize(words):
    """Group words into unbreakable UNITS so no short word/article ends a line.

    A glue word absorbs following words until a non-glue word closes the unit;
    the words in a unit are joined with a non-breaking space, so a wrap can only
    fall BETWEEN units, never after an article or a 1-2 letter word.
    """
    units, i, n = [], 0, len(words)
    while i < n:
        parts = [words[i]]
        while _is_glue(parts[-1]) and (i + len(parts)) < n:
            parts.append(words[i + len(parts)])
        units.append(_NBSP.join(parts))
        i += len(parts)
    return units


def _greedy(widths, space_w, max_w):
    """Greedy first-fit wrap over unit widths. Return lines (lists of indices)."""
    lines, cur, cur_w = [], [], 0.0
    for i, ww in enumerate(widths):
        add = ww if not cur else space_w + ww
        if cur and cur_w + add > max_w:
            lines.append(cur)
            cur, cur_w = [i], ww
        else:
            cur.append(i)
            cur_w += add
    if cur:
        lines.append(cur)
    return lines


def balance_lines(text, max_width_px, size_px, tracking=True, max_lines=None):
    """Return ``text`` typeset into balanced lines (with ``"\n"`` breaks).

    Applies the system's paragraph rules in one place:
      * em-dash -> en-dash (:func:`normalize_dashes`);
      * no widow/orphan and no short word at a line end -- articles and 1-2
        letter words are glued to the next word (NBSP), so the wrap never falls
        after them (:func:`_tokenize`);
      * balanced line lengths -- every line fits ``max_width_px`` and the number
        of lines is the minimum needed, with the longest line minimized so lines
        come out even (never "one long line, then a two-word line").
    Hard ``"\n"`` in ``text`` are preserved and each segment balanced on its own.
    """
    text = normalize_dashes(text)
    if "\n" in text:
        return "\n".join(
            balance_lines(seg, max_width_px, size_px, tracking, max_lines)
            for seg in text.split("\n")
        )

    words = text.split()
    if len(words) <= 1:
        return text
    # A spaced en-dash glues BACKWARD to the previous word (it stays at a line
    # end with the preceding clause, never starts the next line).
    merged = []
    for w in words:
        if w == _EN_DASH and merged:
            merged[-1] = merged[-1] + _NBSP + w
        else:
            merged.append(w)
    words = merged
    units = _tokenize(words)
    if len(units) <= 1:
        return units[0] if units else text

    widths = [text_width_px(u, size_px, tracking) for u in units]
    space_w = char_advance_px(" ", size_px, tracking)
    longest = max(widths)

    # Natural (minimum) line count at the full width.
    L = len(_greedy(widths, space_w, max_width_px))
    if L <= 1:
        return " ".join(units)

    # Binary-search the smallest line width that still wraps into <= L lines;
    # greedy-wrapping there evens the lines out (minimizes the longest line).
    lo, hi = longest, max_width_px
    for _ in range(40):                       # ~40 iters -> sub-px precision
        mid = (lo + hi) / 2.0
        if len(_greedy(widths, space_w, mid)) <= L:
            hi = mid
        else:
            lo = mid
    balanced = _greedy(widths, space_w, hi)

    return "\n".join(" ".join(units[i] for i in line) for line in balanced)


def glue_short_words(text):
    """Insert non-breaking spaces so a line can never END on a short word.

    Same gluing as :func:`balance_lines` (articles / 1-2 letter words bind to the
    next word, a spaced en-dash binds back to the previous word) but WITHOUT
    re-wrapping: word order and hard ``"\n"`` are preserved. Applied to every run
    by ``primitives.add_text`` so ANY text — titles included — that soft-wraps in
    its box never breaks after a short word (R33). Idempotent on already-balanced
    text.
    """
    if "\n" in text:
        return "\n".join(glue_short_words(seg) for seg in text.split("\n"))
    words = text.split()
    if len(words) <= 1:
        return text
    # PRESERVE leading/trailing whitespace: two-tone titles rely on the space at
    # a segment boundary (e.g. "3D content " + "can't ...") -- stripping it would
    # weld adjacent-colour words together.
    lead = text[:len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    merged = []
    for w in words:
        if w == _EN_DASH and merged:
            merged[-1] = merged[-1] + _NBSP + w
        else:
            merged.append(w)
    return lead + " ".join(_tokenize(merged)) + trail


def glue_all_words(text):
    """Bind EVERY word with a non-breaking space so the whole phrase stays on one
    line and wraps as a UNIT. Preserves hard ``"\n"`` and leading/trailing
    whitespace. Used for a two-tone heading's accent run so a multi-word accent
    never splits — one word must not hang at a line end while the rest wraps
    (R37); both move to the next line together.
    """
    if "\n" in text:
        return "\n".join(glue_all_words(seg) for seg in text.split("\n"))
    words = text.split()
    if len(words) <= 1:
        return text
    lead = text[:len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    return lead + _NBSP.join(words) + trail


def line_count(text, max_width_px, size_px, tracking=True):
    """Number of lines ``text`` occupies when wrapped at ``max_width_px``.

    Honours hard ``"\n"`` breaks. Uses the same balanced/greedy wrap as
    :func:`balance_lines`, so callers can size a fixed-height box to the wrapped
    text before drawing it.
    """
    return balance_lines(text, max_width_px, size_px, tracking).count("\n") + 1
