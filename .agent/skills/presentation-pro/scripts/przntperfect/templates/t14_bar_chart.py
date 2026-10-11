"""14 - Bar chart (Figma node 562:41); values below the chart are a NATIVE table.

Resolved (pixel-measured against 14.png): axis hairline at y661; bars bottom at
y648 (they float ~13px above the axis, NOT sitting on it); bar 5 top y112. There
is NO 5th value label -- the shortest High bar is unlabelled and only bars 2-5
carry 30x / 130x / 153x / 351x. The bars, their value labels, the axis line, the
two-tone heading and the footer are unchanged (client scope: don't touch them).

Value table (client-approved, 2026-07-23) -- native ``GraphicFrame`` table
--------------------------------------------------------------------------
The block of values under the chart used to be free text boxes + solid hairline
shapes. It is now a real PowerPoint table so rows/values stay editable, mirroring
the agenda (t02) and the data table (t15).

The reference underlines are NOT one solid rule per row: each column carries its
OWN short segment and there is a ~21px GAP between adjacent columns' segments
(confirmed by the client's Figma screenshot and by pixel-measuring 14.png). The
gaps are produced structurally: the table has 9 columns -- 5 content columns
(the values) interleaved with 4 narrow SPACER columns. Only content cells carry
a bottom border; spacer cells have every border noFill, so the underline breaks
across each spacer's width.

Measured off 14.png (line row y=796), segment [left,right] and gap:
    col1 357-642 | 23 | col2 665-948 | 22 | col3 970-1256 | 21 |
    col4 1277-1563 | 20 | col5 1583-1871
Content left edges 357/665/970/1277/1583 == the bar origins / value-text origins
(so text and segment start share an x). Content widths 285/283/286/286/288 land
each segment's right edge on the measured value; spacer widths 23/22/21/20 fill
the gaps. Column 1's rows 3-4 are empty AND border-less (its segments exist only
under rows 1-2); columns 2-5 carry a segment under all four rows.

Underline colour & weight: the reference lines LOOK light (lum ~216, RGB
211,216,227) and span two pixel rows, but that is a 1px stroke sitting on an
INTEGER pixel boundary and anti-aliased 50/50 with white: 2*211-255=167 ->
(167,177,199) == Gray-Dark #A8B1C7 (the same stroke t02/t15 use; the axis
resolves the same way to Graphite). So the underline is a crisp 1px = 0.5pt
Gray-Dark border, realised via the t02/t15 half-pixel trick: row boundaries sit
on nnn.5 (796.5/861.5/926.5/991.5) so the CENTER-stroked 0.5pt border lands on a
single pixel row instead of smearing across two.

Cell text is styled exactly like primitives.add_text: Arial Regular 32px, exact
spcPts line pitch, -1% tracking (spc=-16), Graphite #454E63. Cells use marT=0 +
anchor="ctr": text is vertically centered in the row (client rule 2026-07-26).
Content col left edge == text origin, so marL=0.
"""

from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

from .. import primitives as P
from .. import composites as C
from ._common import (
    white_bg, light_footer, HIGH, HIGH1, HIGH2, HIGH3, HIGH4, GRAPHITE,
    GREY_LIGHT, GRAY_DARK,
)
from ..units import PXt, tracking_spc

# Axis: the reference shows two soft rows 661-662 at (162,166,177) = a 1px
# GRAPHITE stroke sitting on the 662.0 boundary, AA'd 50/50 (2x161.5-255 =
# Graphite). Rect top 661.5 + 1px height straddles that boundary the same way.
BASELINE_Y = 661.5   # axis hairline top (renders soft rows 661+662, as in ref)
BAR_BOTTOM = 648     # bars float ~13px above the axis line (measured: blue ends 647)

BARS = [
    dict(x=357, width=285, top=569, color=HIGH, value=None),   # unlabelled
    dict(x=665, width=285, top=449, color=HIGH1, value="30x"),
    dict(x=970, width=285, top=318, color=HIGH2, value="130x"),
    dict(x=1277, width=285, top=241, color=HIGH3, value="153x"),
    dict(x=1583, width=285, top=112, color=HIGH4, value="351x"),  # measured top 112
]

# --- native value table ----------------------------------------------------- #
# 9 columns: content (values) interleaved with 4 spacer columns (the gaps). The
# content columns' left edges land on 357/665/970/1277/1583 (== bar / text x).
TABLE_X = 357
TABLE_Y = 731.5                    # row-1 top (no top border -> need not be nnn.5)
#              c1  s1  c2  s2  c3  s3  c4  s4  c5
COL_WIDTHS = [285, 23, 283, 22, 286, 21, 286, 20, 288]
CONTENT_COLS = [0, 2, 4, 6, 8]     # indices of the value columns
NCOLS = 9
NROWS = 4

ROW_H = 65                         # measured row pitch (glyph tops 65px apart)
# Row lower boundaries on the nnn.5 grid so the CENTER-stroked 0.5pt border lands
# on ONE pixel row (t02/t15 half-pixel trick). Reference 1px strokes sit on the
# integer boundaries 797/862/927/992; 796.5/... renders them crisp on rows
# 796/861/926/991 (same ink as the ref's 2-row anti-aliased blur).
# INTEGER boundaries here, unlike t02/t15: this table's reference lines sit ON
# the pixel boundary, anti-aliased 50/50 across two soft rows (796+797 at
# lum~218), not as one crisp row. A stroke centered on the integer boundary
# reproduces exactly that; an nnn.5 boundary gives a crisp single row that
# mismatches BOTH soft rows (verified by pixel diff both ways).
ROW_BOTTOMS = [797, 862, 927, 992]
CELL_SIZE = 32                     # Table-Numbers override (not the 26px of t15)

# Underline: crisp 1px = 0.5pt Gray-Dark #A8B1C7 (see docstring: the reference's
# light-looking 2-row line is this stroke anti-aliased 50/50 with white).
SEP_HEX = str(GRAY_DARK)           # "A8B1C7"
SEP_W_EMU = 6350                   # 0.5pt = 1px

# 4 rows x 5 content columns. "" = empty cell (col 1, rows 3-4 only).
VALUES = [
    ["0.18 msec", "5.13 msec", "23.43 msec", "27.45 msec", "63.18 msec"],
    ["2.3W", "2.4W", "2.35W", "0.63W", "3W"],
    ["", "29x slower", "130x slower", "153x slower", "351x slower"],
    ["", "30x higher", "133x higher", "42x higher", "458x higher"],
]

# "No Style, No Grid" table style -- no header fill, no banding, no gridlines.
NO_STYLE_NO_GRID = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"


def _disable_table_style(table):
    """Kill the default tableStyle (header/banding fills) so cells stay clean."""
    table.first_row = False
    table.last_row = False
    table.first_col = False
    table.last_col = False
    table.horz_banding = False
    table.vert_banding = False
    tblPr = table._tbl.tblPr
    styleId = tblPr.find(qn("a:tableStyleId"))
    if styleId is None:
        styleId = parse_xml(
            '<a:tableStyleId xmlns:a="http://schemas.openxmlformats.org/'
            f'drawingml/2006/main">{NO_STYLE_NO_GRID}</a:tableStyleId>'
        )
        tblPr.append(styleId)
    else:
        styleId.text = NO_STYLE_NO_GRID


def _fill_cell_text(cell, text):
    """Style a cell's text exactly like primitives.add_text (Arial, exact spc)."""
    tf = cell.text_frame
    tf.word_wrap = True
    para = tf.paragraphs[0]
    para.alignment = PP_ALIGN.LEFT
    # Exact line pitch in points (spcPts), never a float multiple. See units.
    para.line_spacing = PXt(CELL_SIZE)                  # 32px * 100%
    if not text:
        return                                          # empty cell: no run
    run = para.add_run()
    run.text = text
    f = run.font
    f.name = "Arial"
    f.size = PXt(CELL_SIZE)
    f.bold = False
    f.italic = False
    f.color.rgb = GRAPHITE
    run._r.get_or_add_rPr().set("spc", str(tracking_spc(CELL_SIZE)))  # -16


def _ln(tag, on):
    """A cell-border XML fragment: the Gray-Dark 0.5pt line, or a no-border."""
    if on:
        return (
            f'<a:{tag} w="{SEP_W_EMU}" cap="flat" cmpd="sng" algn="ctr">'
            f'<a:solidFill><a:srgbClr val="{SEP_HEX}"/></a:solidFill>'
            f'<a:prstDash val="solid"/></a:{tag}>'
        )
    return f'<a:{tag}><a:noFill/></a:{tag}>'


def _set_cell_box(cell, bottom_border):
    """Rewrite the cell's tcPr: zeroed insets, center-anchor, only an optional
    bottom border, noFill.

    marT=0 + anchor="ctr": text is vertically centered in the row
    (client rule 2026-07-26). marL is 0 (content col left edge == text origin).
    lnT/lnL/lnR are explicit no-borders so only each row's own bottom border
    shows, and the fill is noFill so the white slide shows through (incl. every
    spacer column, which has bottom_border=False -> its gap breaks the underline).
    """
    tc = cell._tc
    existing = tc.find(qn("a:tcPr"))
    if existing is not None:
        tc.remove(existing)
    xml = (
        '<a:tcPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'marL="0" marR="0" marT="0" marB="0" anchor="ctr">'
        f'{_ln("lnL", False)}{_ln("lnR", False)}'
        f'{_ln("lnT", False)}{_ln("lnB", bottom_border)}'
        "<a:noFill/>"
        "</a:tcPr>"
    )
    tc.append(parse_xml(xml))          # tcPr follows txBody in CT_TableCell


def build(deck):
    s = deck.add_slide()
    white_bg(s)
    # Two-tone heading rendered as two single-line boxes so the inter-line advance
    # matches the reference. y=54/118 (was 44/108): 64px caps land box_top+4 under
    # the exact-spcPts engine; reference cap tops measured y58/y122 (render y48/y112
    # at 44/108). Both lines shift +10; gap stays 64px. Widths match ref (tracking on).
    P.add_text(s, 50, 54, 1070, 90, "2x More",
               size_px=64, line_height_pct=100, color=HIGH)
    P.add_text(s, 50, 118, 1070, 90, "Efficient For Processing",
               size_px=64, line_height_pct=100, color=GRAPHITE)

    # value_top_offset 33 (was 25): reference value glyphs sit bar_top+37 (measured
    # 486/355/278/149 vs bar tops 449/318/241/112); 48px label lands box_top+4, so
    # offset = 37-4 = 33. Old 25 rendered them bar_top+29 (8px too high).
    C.add_bar_chart(
        s, BARS, BASELINE_Y, baseline_color=GRAPHITE, bar_bottom_px=BAR_BOTTOM,
        value_size_px=48, value_color=GRAPHITE,
        value_top_offset_px=33, value_inset_px=30,
    )

    # --- native value table --------------------------------------------------- #
    row_tops = [TABLE_Y] + ROW_BOTTOMS[:-1]
    row_heights = [ROW_BOTTOMS[i] - row_tops[i] for i in range(NROWS)]

    gf = s.shapes.add_table(
        NROWS, NCOLS,
        PXt(TABLE_X), PXt(TABLE_Y), PXt(sum(COL_WIDTHS)), PXt(sum(row_heights)),
    )
    table = gf.table
    _disable_table_style(table)
    for c in range(NCOLS):
        table.columns[c].width = PXt(COL_WIDTHS[c])

    content_index = {col: i for i, col in enumerate(CONTENT_COLS)}
    for r in range(NROWS):
        table.rows[r].height = PXt(row_heights[r])
        for c in range(NCOLS):
            cell = table.cell(r, c)
            if c in content_index:
                ci = content_index[c]
                text = VALUES[r][ci]
                # Column 1 (first content col) has NO underline on rows 3-4 (its
                # segments exist only under rows 1-2); all other content cols
                # underline every row. Spacer columns never underline.
                has_line = not (ci == 0 and r >= 2)
                _fill_cell_text(cell, text)
                _set_cell_box(cell, has_line)
            else:
                # spacer column: empty, no borders -> creates the inter-column gap
                _fill_cell_text(cell, "")
                _set_cell_box(cell, False)

    light_footer(s)
    return s
