"""bbox-visualizer - Different ways of visualizing objects given bounding box data."""

from ._version import __version__
from .core import (
    draw_rectangle,
    draw_multiple_rectangles,
    add_label,
    add_multiple_labels,
    add_T_label,
    add_multiple_T_labels,
    draw_flag_with_label,
    draw_multiple_flags_with_labels,
)

__all__ = [
    "__version__",
    "draw_rectangle",
    "draw_multiple_rectangles",
    "add_label",
    "add_multiple_labels",
    "add_T_label",
    "add_multiple_T_labels",
    "draw_flag_with_label",
    "draw_multiple_flags_with_labels",
]

__author__ = """Shoumik Sharar Chowdhury"""
__email__ = "shoumikchow@gmail.com"
