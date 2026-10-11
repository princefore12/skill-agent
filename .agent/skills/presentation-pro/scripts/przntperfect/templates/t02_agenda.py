"""02 - Agenda (Figma node 562:185), rendered as a NATIVE PowerPoint table.

Client-approved exception to the "text + lines" rule: the agenda is a real
``GraphicFrame`` table object so items can be added/removed as table rows, and
each row carries an underline (its bottom border). The geometry reproduces the
previous text+hairline render exactly (that render matched the reference to
1.22%):

* 6 horizontal separators at y = 471/575/679/783/887/991 (measured on the
  reference) -- realised as the table's top border (row 0) plus each row's
  bottom border. Colour Gray-Dark #A8B1C7, 0.5pt (=1px). No other borders.
* Every cell margin is zeroed, then re-set so the text ORIGIN matches the old
  textboxes 1:1: number origin x=52px (glyph ~x53), label origin x=199px
  (glyph ~x201), text-area top = row_top + 31px (48px cap lands row_top+35).
* Arial Regular 48px (24pt), Semi-Light, -1% tracking (rPr@spc=-24), exact
  spcPts line pitch -- identical run styling to primitives.add_text.
* The default table style (header/banding fills) is disabled: firstRow/bandRow
  off and styleId set to "No Style, No Grid"; every cell is noFill.

The "Agenda" H1 title is unchanged.
"""

from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

from .. import primitives as P
from ._common import GRAPHITE, SEMI_LIGHT, GRAY_DARK
from ..units import PXt, tracking_spc

ITEMS = [
    ("01", "Seeing beyond"),
    ("02", "Where others see randomness"),
    ("03", "Unlocks new levels of control"),
    ("04", "Manufacturing and defense"),
    ("05", "Q&A session"),
]

# --- table geometry (px on the 1920x1080 canvas) ---------------------------- #
# TABLE_Y is nudged +0.5px: PowerPoint strokes table borders CENTERED on the
# row boundary, smearing a 0.5pt line across two pixel rows (470-471). With
# boundaries at nnn.5 the stroke lands exactly on the reference's single row
# (471/575/.../991). Text shifts sub-pixel only (anti-aliasing).
TABLE_X, TABLE_Y = 50, 471.5
TABLE_W = 1820
# 104px (=52pt) rows land the 6 separators exactly on the measured reference
# y's (471, 575, 679, 783, 887, 991); the row height is the MINIMUM and wins
# because the single 24pt line of content is shorter than it.
ROW_H = 104
COL1_W = 149               # -> column 2 (label) left edge at x=199
NUM_MARL_PX = 2            # cell x50 + 2px -> number origin x52 (== old textbox)
LAB_MARL_PX = 0            # cell x199 + 0  -> label origin x199 (== old textbox)

FONT_PX = 48
SEP_HEX = str(GRAY_DARK)   # "A8B1C7"
SEP_W_EMU = 6350           # 0.5pt = 1px
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


def _fill_cell_text(cell, text, color):
    """Style a cell's text exactly like primitives.add_text (Arial, exact spc)."""
    tf = cell.text_frame
    tf.word_wrap = True
    para = tf.paragraphs[0]
    para.alignment = PP_ALIGN.LEFT
    # Exact line pitch in points (spcPts) -- never a float multiple. See units.
    para.line_spacing = PXt(FONT_PX)          # 48px * 100% -> Pt(24)
    run = para.add_run()
    run.text = text
    f = run.font
    f.name = "Arial"
    f.size = PXt(FONT_PX)                      # 24pt
    f.bold = False
    f.italic = False
    f.color.rgb = color
    run._r.get_or_add_rPr().set("spc", str(tracking_spc(FONT_PX)))  # -24


def _ln(tag, on):
    """A cell-border XML fragment: the separator line, or an explicit no-border."""
    if on:
        return (
            f'<a:{tag} w="{SEP_W_EMU}" cap="flat" cmpd="sng" algn="ctr">'
            f'<a:solidFill><a:srgbClr val="{SEP_HEX}"/></a:solidFill>'
            f'<a:prstDash val="solid"/></a:{tag}>'
        )
    return f'<a:{tag}><a:noFill/></a:{tag}>'


def _set_cell_box(cell, marL_px, top_border, bottom_border):
    """Rewrite the cell's tcPr: zeroed margins + insets, center-anchor, borders, noFill.

    Only the top border (row 0) and each row's bottom border are drawn; left,
    right and remaining top borders are explicit no-borders, and the cell fill
    is noFill so the Graphite slide background shows through.

    marT=0 + anchor="ctr": text is vertically centered in the row
    (client rule 2026-07-26). marL keeps the number/label horizontal insets.
    """
    tc = cell._tc
    existing = tc.find(qn("a:tcPr"))
    if existing is not None:
        tc.remove(existing)
    marL = int(PXt(marL_px))          # EMU
    xml = (
        '<a:tcPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        f'marL="{marL}" marR="0" marT="0" marB="0" anchor="ctr">'
        f'{_ln("lnL", False)}{_ln("lnR", False)}'
        f'{_ln("lnT", top_border)}{_ln("lnB", bottom_border)}'
        "<a:noFill/>"
        "</a:tcPr>"
    )
    tc.append(parse_xml(xml))          # tcPr follows txBody in CT_TableCell


def build(deck):
    s = deck.add_slide()
    P.add_solid_background(s, GRAPHITE)

    # Title "Agenda" -- unchanged (H1 64px, Semi-Light).
    P.add_text(s, 50, 72, 600, 100, "Agenda", size_px=64, line_height_pct=100,
               color=SEMI_LIGHT)

    rows = len(ITEMS)
    gf = s.shapes.add_table(
        rows, 2, PXt(TABLE_X), PXt(TABLE_Y), PXt(TABLE_W), PXt(ROW_H * rows)
    )
    table = gf.table
    _disable_table_style(table)
    table.columns[0].width = PXt(COL1_W)
    table.columns[1].width = PXt(TABLE_W - COL1_W)

    for r, (num, label) in enumerate(ITEMS):
        table.rows[r].height = PXt(ROW_H)
        first = (r == 0)                       # only row 0 carries a top border
        c_num, c_lab = table.cell(r, 0), table.cell(r, 1)
        _fill_cell_text(c_num, num, SEMI_LIGHT)
        _fill_cell_text(c_lab, label, SEMI_LIGHT)
        _set_cell_box(c_num, NUM_MARL_PX, first, True)
        _set_cell_box(c_lab, LAB_MARL_PX, first, True)
    return s
