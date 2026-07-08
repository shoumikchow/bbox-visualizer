"""Multiple-objects bbox-visualizer example.

Loads an image with several annotations and renders all objects using each of
bbox-visualizer's multi-object label styles.

Run from the repo root:
    python examples/multiple_objects.py
"""

import json
from pathlib import Path

import cv2

import bbox_visualizer as bbv

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGE_PATH = REPO_ROOT / "images" / "source_multiple.jpg"
ANNOTATION_PATH = REPO_ROOT / "images" / "source_multiple.json"
OUT_DIR = Path(__file__).parent / "output"


def load_annotations(path: Path) -> tuple[list[list[int]], list[str]]:
    """Read a labelme-style annotation, return (bboxes, labels) as parallel lists."""
    data = json.loads(path.read_text())
    bboxes: list[list[int]] = []
    labels: list[str] = []
    for shape in data["shapes"]:
        (xmin, ymin), (xmax, ymax) = shape["points"]
        bboxes.append([xmin, ymin, xmax, ymax])
        labels.append(shape["label"])
    return bboxes, labels


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    base = cv2.imread(str(IMAGE_PATH))
    bboxes, labels = load_annotations(ANNOTATION_PATH)

    # 1. Multiple boxes + labels on top
    img = base.copy()
    img = bbv.draw_multiple_boxes(img, bboxes)
    img = bbv.add_multiple_labels(img, labels, bboxes)
    cv2.imwrite(str(OUT_DIR / "multiple_top.jpg"), img)

    # 2. Multiple boxes + T-shaped labels
    img = base.copy()
    img = bbv.draw_multiple_boxes(img, bboxes)
    img = bbv.add_multiple_T_labels(img, labels, bboxes)
    cv2.imwrite(str(OUT_DIR / "multiple_t.jpg"), img)

    # 3. Multiple flag-style labels (no separate boxes)
    img = base.copy()
    img = bbv.draw_multiple_flags_with_labels(img, labels, bboxes)
    cv2.imwrite(str(OUT_DIR / "multiple_flags.jpg"), img)

    print(f"Wrote 3 variants to {OUT_DIR}")


if __name__ == "__main__":
    main()
