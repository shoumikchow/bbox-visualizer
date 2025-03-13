"""Core functionality for bbox-visualizer."""

from .flags import (
    add_multiple_T_labels,
    add_T_label,
    draw_flag_with_label,
    draw_multiple_flags_with_labels,
)
from .labels import add_label, add_multiple_labels
from .rectangle import draw_multiple_rectangles, draw_rectangle

__all__ = [
    "add_T_label",
    "add_label",
    "add_multiple_T_labels",
    "add_multiple_labels",
    "draw_flag_with_label",
    "draw_multiple_flags_with_labels",
    "draw_multiple_rectangles",
    "draw_rectangle",
]
