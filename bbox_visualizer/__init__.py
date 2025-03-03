"""Top-level package for bbox-visualizer."""

from ._version import __version__

__author__ = """Shoumik Sharar Chowdhury"""
__email__ = 'shoumikchow@gmail.com'

from .bbox_visualizer import (
    draw_rectangle, 
    add_label, 
    add_T_label, 
    draw_flag_with_label, 
    add_multiple_labels, 
    add_multiple_T_labels, 
    draw_multiple_rectangles, 
    draw_multiple_flags_with_labels
    )
