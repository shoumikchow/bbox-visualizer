"""Label stress-test for bbox-visualizer.

Renders a grid of boxes with deliberately awkward label strings (all caps,
descenders only, punctuation, a very long word, ...) through each label
style, plus a font-size sweep. Useful for eyeballing label layout changes.

Run from the repo root:
    python examples/label_stress.py
"""

from collections.abc import Callable, Iterator
from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray

import bbox_visualizer as bbv

OUT_DIR = Path(__file__).parent / "output"

LABELS = [
    "person",  # lowercase + descender
    "PERSON",  # all caps, no descenders
    "Person",  # mixed case
    "jjggyy",  # descenders only
    "flying high",  # ascenders + descenders + space
    "a",  # single short char
    "99.9%",  # digits + punctuation
    "traffic_light",  # underscore (COCO-style class name)
    "floccinaucinihilipilification",  # very long word
]

CELL_W, CELL_H, COLS = 530, 300, 3
ROWS = (len(LABELS) + COLS - 1) // COLS
GREEN = (0, 255, 0)

Image = NDArray[np.uint8]


def cells() -> Iterator[tuple[str, list[int]]]:
    """Yield (label, bbox) pairs laid out on a grid."""
    for i, label in enumerate(LABELS):
        ox, oy = (i % COLS) * CELL_W, (i // COLS) * CELL_H
        yield label, [ox + 60, oy + 130, ox + 260, oy + 270]


def render(style: str, add_label: Callable[[Image, str, list[int]], Image]) -> None:
    """Draw every stress label with one label style and save the grid."""
    img: Image = np.full((ROWS * CELL_H, COLS * CELL_W, 3), 60, dtype=np.uint8)
    for label, bbox in cells():
        img = bbv.draw_rectangle(img, bbox, bbox_color=GREEN, thickness=2)
        img = add_label(img, label, bbox)
    cv2.imwrite(str(OUT_DIR / f"label_stress_{style}.jpg"), img)


def render_sizes() -> None:
    """Sweep font sizes on a label with a descender."""
    img: Image = np.full((320, 1600, 3), 60, dtype=np.uint8)
    for size, x in [(0.5, 40), (1, 400), (1.5, 800), (2, 1250)]:
        bbox = [x, 150, x + 300, 290]
        img = bbv.draw_rectangle(img, bbox, bbox_color=GREEN, thickness=2)
        img = bbv.add_label(img, f"size {size}g", bbox, size=size)
    cv2.imwrite(str(OUT_DIR / "label_stress_sizes.jpg"), img)


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    render("top", lambda img, label, bbox: bbv.add_label(img, label, bbox))
    render(
        "inside", lambda img, label, bbox: bbv.add_label(img, label, bbox, top=False)
    )
    render("t", lambda img, label, bbox: bbv.add_T_label(img, label, bbox))
    render(
        "flag",
        lambda img, label, bbox: bbv.draw_flag_with_label(
            img, label, bbox, line_color=GREEN
        ),
    )
    render_sizes()
    print(f"Wrote 5 stress images to {OUT_DIR}")


if __name__ == "__main__":
    main()
