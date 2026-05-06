"""Minimal bbox-visualizer example.

Draws a single labeled bounding box on a blank canvas and saves the result.
No external image required.

Run from the repo root:
    python examples/quickstart.py
"""

from pathlib import Path

import cv2
import numpy as np

import bbox_visualizer as bbv

OUT_PATH = Path(__file__).parent / "output" / "quickstart.jpg"


def main() -> None:
    OUT_PATH.parent.mkdir(exist_ok=True)

    img = np.full((400, 600, 3), 40, dtype=np.uint8)

    # Bounding box format: [x_min, y_min, x_max, y_max]
    bbox = [150, 100, 450, 300]
    label = "object"

    img = bbv.draw_box(img, bbox, bbox_color=(0, 255, 0))
    img = bbv.add_label(img, label, bbox)

    cv2.imwrite(str(OUT_PATH), img)
    print(f"Saved {OUT_PATH}")


if __name__ == "__main__":
    main()
