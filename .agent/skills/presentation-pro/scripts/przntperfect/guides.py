"""Presentation-level layout guides on the Prznt Perfect 12-col / 26-row grid.

PowerPoint stores editor guides in the ``/ppt/viewProps.xml`` part, under
``p:viewPr/p:slideViewPr/p:cSldViewPr/p:guideLst``. Each ``p:guide`` is one
guide line:

* ``<p:guide pos="P"/>``               -- a VERTICAL guide (orient defaults to
  vertical) at horizontal position ``P``.
* ``<p:guide orient="horz" pos="P"/>`` -- a HORIZONTAL guide at vertical
  position ``P``.

``pos`` is measured in **1/8 pt**. A px coordinate on the 1920x1080 design canvas
converts as ``pos = px * PX_TO_PT * 8 = px * 0.5 * 8 = px * 4`` (e.g. x=50px ->
25pt -> pos=200). Column/row geometry comes from the COMPUTED grid widths in
``design-tokens.json`` (see grid.py / tokens.py), not the stated-but-non-closing
135px / 23px figures.
"""

from lxml import etree
from pptx.oxml.ns import qn

from .grid import GRID
from .tokens import TOKENS

_P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
_VIEWPROPS_PARTNAME = "/ppt/viewProps.xml"

# 1/8-pt per design px:  px -> pt (x0.5) -> 1/8 pt (x8)  ==  px x 4.
_POS_PER_PX = 4


def _pos(px):
    """Design-px coordinate -> guide ``pos`` value (1/8 pt, integer)."""
    return int(round(px * _POS_PER_PX))


# --------------------------------------------------------------------------- #
# geometry
# --------------------------------------------------------------------------- #
def _positions(cols, rows, margins):
    """Return ``(vert_pos_list, horz_pos_list)`` as sorted, de-duplicated ints.

    * cols   -> BOTH edges (left + right) of every one of the 12 columns
                (24 vertical guides). Each pair frames a 133.333px column; the
                20px space between one column's right edge and the next column's
                left edge is the gutter, so the grid reads as 12 columns WITH
                gutters rather than 12 bare edge ticks.
    * rows   -> the 26 row boundaries, i.e. the top of each row plus the bottom
                of the last row (27 horizontal guides).
    * margins-> the top and bottom page margins (2 horizontal guides).
    """
    verts, horzs = [], []

    if cols:
        # left_i  = 50 + i*153.333  ;  right_i = left_i + 133.333  (i = 0..11)
        for i in range(TOKENS.col_count):            # 24 column edges (12 pairs)
            verts.append(GRID.col_x(i))              # left edge
            verts.append(GRID.col_right(i))          # right edge (col 11 -> 1870)

    if rows:
        for i in range(TOKENS.row_count):            # 26 row tops
            horzs.append(GRID.row_y(i))
        horzs.append(GRID.row_bottom(TOKENS.row_count - 1))   # last row bottom (1030)

    if margins:
        horzs.append(TOKENS.margin_px)                        # top margin (50)
        horzs.append(TOKENS.margin_px + TOKENS.content_h_px)  # bottom margin (1030)

    vpos = sorted(dict.fromkeys(_pos(x) for x in verts))
    hpos = sorted(dict.fromkeys(_pos(y) for y in horzs))
    return vpos, hpos


# --------------------------------------------------------------------------- #
# viewProps.xml part access
# --------------------------------------------------------------------------- #
def _find_viewprops_part(prs):
    for part in prs.part.package.iter_parts():
        if str(part.partname) == _VIEWPROPS_PARTNAME:
            return part
    return None


def _create_viewprops_part(prs):
    """Create an empty ``/ppt/viewProps.xml`` part and relate it to the deck.

    Only needed if a template ships without one; the stock python-pptx template
    already includes it, so this is a safety net.
    """
    from pptx.opc.package import Part
    from pptx.opc.packuri import PackURI
    from pptx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT

    skeleton = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<p:viewPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        f'xmlns:p="{_P_NS}">'
        "<p:slideViewPr><p:cSldViewPr>"
        '<p:cViewPr varScale="1">'
        '<p:scale><a:sx n="100" d="100"/><a:sy n="100" d="100"/></p:scale>'
        '<p:origin x="0" y="0"/>'
        "</p:cViewPr>"
        "</p:cSldViewPr></p:slideViewPr></p:viewPr>"
    ).encode("utf-8")

    part = Part(PackURI(_VIEWPROPS_PARTNAME), CT.PML_VIEW_PROPS,
                prs.part.package, skeleton)
    prs.part.relate_to(part, RT.VIEW_PROPS)
    return part


def _ensure_cSldViewPr(root):
    """Return the ``p:cSldViewPr`` element, building the parent chain if absent."""
    slideViewPr = root.find(qn("p:slideViewPr"))
    if slideViewPr is None:
        slideViewPr = etree.SubElement(root, qn("p:slideViewPr"))
    cSld = slideViewPr.find(qn("p:cSldViewPr"))
    if cSld is None:
        cSld = etree.SubElement(slideViewPr, qn("p:cSldViewPr"))
    if cSld.find(qn("p:cViewPr")) is None:
        # cViewPr (scale + origin) is required to precede guideLst in the schema.
        cView = etree.SubElement(cSld, qn("p:cViewPr"))
        cView.set("varScale", "1")
        scale = etree.SubElement(cView, qn("p:scale"))
        sx = etree.SubElement(scale, qn("a:sx")); sx.set("n", "100"); sx.set("d", "100")
        sy = etree.SubElement(scale, qn("a:sy")); sy.set("n", "100"); sy.set("d", "100")
        origin = etree.SubElement(cView, qn("p:origin"))
        origin.set("x", "0"); origin.set("y", "0")
    return cSld


# --------------------------------------------------------------------------- #
# public entry point
# --------------------------------------------------------------------------- #
def add_grid_guides(prs, cols=True, rows=False, margins=True, show=False):
    """Write Prznt Perfect grid guides into the presentation's ``viewProps.xml``.

    Replaces any pre-existing ``guideLst`` (the stock template ships two demo
    guides) with the Prznt Perfect set. With the defaults this emits 24 vertical
    guides -- both edges of every one of the 12 columns, so the 20px gutters are
    visible -- plus 2 horizontal margin guides (y50 / y1030). Guides are OFF by
    default (client decision 2026-07-23): they ship in the file but stay
    invisible until the user turns on View -> Guides. Pass ``show=True`` to open
    with guides visible. Returns a dict ``{"vert": [...pos], "horz": [...pos]}``
    of the emitted guide positions (1/8 pt) for verification/logging.
    """
    vpos, hpos = _positions(cols, rows, margins)

    part = _find_viewprops_part(prs)
    if part is None:
        part = _create_viewprops_part(prs)

    root = etree.fromstring(part.blob)
    cSld = _ensure_cSldViewPr(root)

    # Drop existing guide list(s), then append a fresh one after cViewPr.
    for old in cSld.findall(qn("p:guideLst")):
        cSld.remove(old)
    guideLst = etree.SubElement(cSld, qn("p:guideLst"))
    for p in vpos:                                    # vertical (orient omitted = default)
        g = etree.SubElement(guideLst, qn("p:guide"))
        g.set("pos", str(p))
    for p in hpos:                                    # horizontal
        g = etree.SubElement(guideLst, qn("p:guide"))
        g.set("orient", "horz")
        g.set("pos", str(p))

    cSld.set("showGuides", "1" if show else "0")

    part._blob = etree.tostring(
        root, xml_declaration=True, encoding="UTF-8", standalone=True
    )
    return {"vert": vpos, "horz": hpos}
