"""The 15 canonical template generators, one module per template.

Each module exposes ``build(deck)`` which adds exactly one slide and returns it.
``BUILDERS`` is the ordered list used by the deck assembler.
"""

from . import (
    t01_cover, t02_agenda, t03_section_light, t04_section_white, t05_section_navy,
    t06_text_image, t07_text_image, t08_text_image, t09_text_image,
    t10_segment_cards, t11_heading_body_image, t12_heading_bodies_image,
    t13_image_blocks, t14_bar_chart, t15_data_table,
)

BUILDERS = [
    t01_cover.build,
    t02_agenda.build,
    t03_section_light.build,
    t04_section_white.build,
    t05_section_navy.build,
    t06_text_image.build,
    t07_text_image.build,
    t08_text_image.build,
    t09_text_image.build,
    t10_segment_cards.build,
    t11_heading_body_image.build,
    t12_heading_bodies_image.build,
    t13_image_blocks.build,
    t14_bar_chart.build,
    t15_data_table.build,
]

__all__ = ["BUILDERS"]
