"""bbox-visualizer - Different ways of visualizing objects given bounding box data."""

from importlib.metadata import version

from .core import (
    add_label,
    add_multiple_labels,
    add_multiple_T_labels,
    add_T_label,
    draw_flag_with_label,
    draw_multiple_flags_with_labels,
    draw_multiple_rectangles,
    draw_rectangle,
    suppress_warnings,
    warnings_suppressed,
)

__version__ = version("bbox_visualizer")

__all__ = [
    "__version__",
    "add_T_label",
    "add_label",
    "add_multiple_T_labels",
    "add_multiple_labels",
    "draw_flag_with_label",
    "draw_multiple_flags_with_labels",
    "draw_multiple_rectangles",
    "draw_rectangle",
    "suppress_warnings",
    "warnings_suppressed",
]

__author__ = """Shoumik Sharar Chowdhury"""
__email__ = "shoumikchow@gmail.com"
