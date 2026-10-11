"""Prznt Perfect Slides -- a PowerPoint generator for the Prznt Perfect design system.

Public surface:
    Deck                     -- 16:9 presentation wrapper
    Tokens / TOKENS          -- design-token accessor (source of truth)
    Grid / GRID              -- 12-col / 26-row grid helper
    units                    -- px<->pt conversion and tracking
    primitives               -- backgrounds, text, two-tone, placeholder, footer, hairline
    composites               -- bar chart & pseudo-table (shapes/text/lines only)
    cards                    -- sanctioned row-of-cards component (add_card_row)
"""

from .deck import Deck
from .tokens import Tokens, TOKENS
from .grid import Grid, GRID
from . import (units, primitives, composites, cards, theme, tables,
               textbalance, components)

__all__ = [
    "Deck", "Tokens", "TOKENS", "Grid", "GRID",
    "units", "primitives", "composites", "cards", "theme", "tables",
    "textbalance", "components",
]
