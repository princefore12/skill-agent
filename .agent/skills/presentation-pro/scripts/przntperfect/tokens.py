"""Design-token loader for the Prznt Perfect Slides engine.

Loads ``references/design-tokens.json`` (the single source of truth) and exposes
colors, typography styles and the computed grid geometry. Nothing here is
hard-coded that could instead be read from the JSON; the JSON is never mutated.
"""

import json
import os

from pptx.dml.color import RGBColor

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOKENS_PATH = os.path.normpath(
    os.path.join(_HERE, "..", "..", "references", "design-tokens.json")
)


def _load_json(path=_TOKENS_PATH):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _rgb(hex_str):
    """'#161A22' or '161A22' -> RGBColor."""
    return RGBColor.from_string(hex_str.lstrip("#").upper())


class Tokens:
    """Typed accessor over design-tokens.json."""

    def __init__(self, data=None):
        self.data = data if data is not None else _load_json()

        # --- colors: name -> RGBColor / hex ---
        self._colors = {
            name: _rgb(spec["hex"]) for name, spec in self.data["colors"].items()
        }
        self._hex = {name: spec["hex"] for name, spec in self.data["colors"].items()}

        # --- typography ---
        self.typography = self.data["typography"]
        self.styles = self.typography["styles"]
        self.chart_series = self.data["chart_series_order"]

        # --- computed grid geometry (px) ---
        grid = self.data["grid"]
        self.margin_px = grid["margins_px"]
        self.content_w_px = grid["content_area_px"]["width"]
        self.content_h_px = grid["content_area_px"]["height"]
        cols = grid["columns"]
        rows = grid["rows"]
        self.col_count = cols["count"]
        self.col_gutter_px = cols["gutter_px"]
        # Rules06 states 135px but does not close; compute the true width.
        self.col_width_px = (
            self.content_w_px - (self.col_count - 1) * self.col_gutter_px
        ) / self.col_count
        self.row_count = rows["count"]
        self.row_gutter_px = rows["gutter_px"]
        self.row_height_px = (
            self.content_h_px - (self.row_count - 1) * self.row_gutter_px
        ) / self.row_count

        # --- canvas / cover gradient / footer ---
        self.canvas = self.data["meta"]["canvas"]
        self.cover_gradient = self.data["effects"]["cover_gradient"]
        self.footer = self.data["footer"]

    # ---- color helpers ----
    def color(self, name):
        """RGBColor for a palette name (e.g. 'High')."""
        return self._colors[name]

    def hex(self, name):
        return self._hex[name]

    # ---- typography helpers ----
    def style(self, name):
        """Return a style dict, e.g. {'size_px':64,'line_height_pct':100,...}."""
        return self.styles[name]

    def size_px(self, name):
        return self.styles[name]["size_px"]

    def line_height_pct(self, name):
        return self.styles[name]["line_height_pct"]


# A shared default instance for convenience.
TOKENS = Tokens()
