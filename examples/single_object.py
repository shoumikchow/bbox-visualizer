"""Single-object bbox-visualizer example.

Loads an image and a labelme-style JSON annotation, then renders the same
object using each of bbox-visualizer's single-object label styles.

Run from the repo root:
    python examples/single_object.py
"""

import json
from pathlib import Path

import cv2

import bbox_visualizer as bbv

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGE_PATH = REPO_ROOT / "images" / "source_single.jpg"
ANNOTATION_PATH = REPO_ROOT / "images" / "source_single.json"
OUT_DIR = Path(__file__).parent / "output"


def load_annotation(path: Path) -> tuple[list[int], str]:
    """Read a labelme-style annotation, return (bbox, label)."""
    data = json.loads(path.read_text())
    shape = data["shapes"][0]
    (xmin, ymin), (xmax, ymax) = shape["points"]
    return [xmin, ymin, xmax, ymax], shape["label"]


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    base = cv2.imread(str(IMAGE_PATH))
    bbox, label = load_annotation(ANNOTATION_PATH)

    # 1. Box + label on top (default style)
    img = base.copy()
    img = bbv.draw_box(img, bbox)
    img = bbv.add_label(img, label, bbox, top=True)
    cv2.imwrite(str(OUT_DIR / "single_top.jpg"), img)

    # 2. Box + label inside
    img = base.copy()
    img = bbv.draw_box(img, bbox)
    img = bbv.add_label(img, label, bbox, top=False)
    cv2.imwrite(str(OUT_DIR / "single_inside.jpg"), img)

    # 3. Box + T-shaped label
    img = base.copy()
    img = bbv.draw_box(img, bbox)
    img = bbv.add_T_label(img, label, bbox)
    cv2.imwrite(str(OUT_DIR / "single_t.jpg"), img)

    # 4. Flag-style label (no separate box)
    img = base.copy()
    img = bbv.draw_flag_with_label(img, label, bbox)
    cv2.imwrite(str(OUT_DIR / "single_flag.jpg"), img)

    # 5. Opaque overlay with label inside
    img = base.copy()
    img = bbv.draw_box(img, bbox, is_opaque=True)
    img = bbv.add_label(img, label, bbox, draw_bg=False, top=False)
    cv2.imwrite(str(OUT_DIR / "single_opaque.jpg"), img)

    print(f"Wrote 5 variants to {OUT_DIR}")


if __name__ == "__main__":
    main()
