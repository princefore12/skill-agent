"""Brand theme colors for the Prznt Perfect design system.

PowerPoint stores the palette shown in the color picker's *Theme Colors* row in
``/ppt/theme/themeN.xml`` under ``a:theme/a:themeElements/a:clrScheme``. The
stock python-pptx template ships the generic "Office" scheme (blue/red/green/…).
This module overwrites that scheme with the Prznt Perfect palette so that every
generated deck offers the design-system colors — and nothing off-brand — the
moment the user opens any color dropdown.

The scheme has 12 fixed slots in this exact child order::

    dk1  lt1  dk2  lt2  accent1..accent6  hlink  folHlink

which the picker surfaces as: Background 1 (lt1), Text 1 (dk1), Background 2
(lt2), Text 2 (dk2), then Accent 1–6. ``hlink``/``folHlink`` are the
hyperlink colors and are not shown as swatches in that row.

Mapping (client request 2026-08-05, keyed to the "Color System" board — the 9
canonical colors, White excluded per the request and kept only as the lt1
background):

===========  ============  =========  ==================================
theme slot   token         hex        picker label
===========  ============  =========  ==================================
lt1          White         #FFFFFF    Background 1  (the excluded white)
dk1          Black         #161A22    Text 1
lt2          White-Cool    #EDEFF2    Background 2
dk2          Navy          #071A3C    Text 2
accent1      High          #00A1FF    Accent 1  (primary brand accent)
accent2      Graphite      #454E63    Accent 2
accent3      Gray-Dark     #A8B1C7    Accent 3
accent4      Grey-Light    #CCD1DB    Accent 4
accent5      Semi-Light    #DEE6FB    Accent 5
accent6      High-1        #75C3F0    Accent 6  (chart tone 2 — see note)
hlink        High          #00A1FF    (hyperlink)
folHlink     Graphite      #454E63    (followed hyperlink)
===========  ============  =========  ==================================

Note: the board carries 8 non-white colors but the scheme has 9 chromatic slots
(dk1, dk2, lt2, accent1–6) once White takes lt1, so one accent is left over.
accent6 is filled with High-1 (#75C3F0) — the second tone of the documented
chart ramp — giving a lighter blue that complements the primary High. Existing
templates paint with explicit sRGB (RGBColor), never scheme references, so this
changes only the picker palette, not any rendered pixel.
"""

from lxml import etree
from pptx.oxml.ns import qn

from .tokens import TOKENS

THEME_NAME = "Prznt Perfect"

#: theme-slot -> palette token name, in the schema-required child order.
COLOR_MAP = [
    ("dk1", "Black"),
    ("lt1", "White"),
    ("dk2", "Navy"),
    ("lt2", "White-Cool"),
    ("accent1", "High"),
    ("accent2", "Graphite"),
    ("accent3", "Gray-Dark"),
    ("accent4", "Grey-Light"),
    ("accent5", "Semi-Light"),
    ("accent6", "High-1"),
    ("hlink", "High"),
    ("folHlink", "Graphite"),
]

_THEME_PARTNAME_PREFIX = "/ppt/theme/"


def _srgb_hex(tokens, token_name):
    """Palette token name -> bare uppercase 6-hex string (no '#')."""
    return tokens.hex(token_name).lstrip("#").upper()


def _build_clrScheme(tokens):
    """Return a fresh ``a:clrScheme`` element carrying the brand palette."""
    scheme = etree.Element(qn("a:clrScheme"))
    scheme.set("name", THEME_NAME)
    for slot, token_name in COLOR_MAP:
        slot_el = etree.SubElement(scheme, qn("a:" + slot))
        srgb = etree.SubElement(slot_el, qn("a:srgbClr"))
        srgb.set("val", _srgb_hex(tokens, token_name))
    return scheme


def _iter_theme_parts(prs):
    for part in prs.part.package.iter_parts():
        if str(part.partname).startswith(_THEME_PARTNAME_PREFIX):
            yield part


def apply_brand_theme(prs, tokens=TOKENS):
    """Overwrite every theme's color scheme with the Prznt Perfect palette.

    Replaces the ``a:clrScheme`` (and sets the theme name) in each
    ``/ppt/theme/themeN.xml`` part so the PowerPoint color picker offers only
    design-system colors. Returns a list of ``(partname, {slot: hex})`` for
    verification/logging.
    """
    results = []
    for part in _iter_theme_parts(prs):
        root = etree.fromstring(part.blob)
        root.set("name", THEME_NAME)

        theme_elements = root.find(qn("a:themeElements"))
        if theme_elements is None:
            continue
        old = theme_elements.find(qn("a:clrScheme"))
        new = _build_clrScheme(tokens)
        if old is not None:
            theme_elements.replace(old, new)
        else:
            theme_elements.insert(0, new)

        part._blob = etree.tostring(
            root, xml_declaration=True, encoding="UTF-8", standalone=True
        )
        results.append(
            (
                str(part.partname),
                {slot: _srgb_hex(tokens, name) for slot, name in COLOR_MAP},
            )
        )
    return results


def read_clrScheme(prs):
    """Return ``[(partname, name, {slot: hex}), …]`` for each theme part.

    Diagnostic helper: reads back the color scheme actually stored in the file
    (used by the linter / verification, not by generation).
    """
    out = []
    for part in _iter_theme_parts(prs):
        root = etree.fromstring(part.blob)
        scheme = root.find(qn("a:themeElements") + "/" + qn("a:clrScheme"))
        if scheme is None:
            continue
        colors = {}
        for slot_el in scheme:
            slot = etree.QName(slot_el).localname
            inner = slot_el[0]
            colors[slot] = inner.get("val") or inner.get("lastClr")
        out.append((str(part.partname), scheme.get("name"), colors))
    return out
