"""Core functionality for bbox-visualizer."""

from .rectangle import draw_rectangle, draw_multiple_rectangles
from .labels import add_label, add_multiple_labels
from .flags import (
    add_T_label,
    add_multiple_T_labels,
    draw_flag_with_label,
    draw_multiple_flags_with_labels,
)

__all__ = [
    "draw_rectangle",
    "draw_multiple_rectangles",
    "add_label",
    "add_multiple_labels",
    "add_T_label",
    "add_multiple_T_labels",
    "draw_flag_with_label",
    "draw_multiple_flags_with_labels",
]
