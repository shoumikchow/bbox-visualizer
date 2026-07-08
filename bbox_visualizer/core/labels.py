"""Functions for adding text labels to bounding boxes."""

from collections.abc import Sequence

import cv2
import numpy as np
from numpy.typing import NDArray

from ._utils import _check_and_modify_bbox, _get_text_size, _validate_color

font = cv2.FONT_HERSHEY_SIMPLEX


def add_label(
    img: NDArray[np.uint8],
    label: str,
    bbox: Sequence[float],
    size: float = 1,
    thickness: int = 2,
    draw_bg: bool = True,
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
    top: bool = True,
    bbox_format: str = "voc",
) -> NDArray[np.uint8]:
    """Add a label to a bounding box, either above or inside it.

    If there isn't enough space above the box, the label is placed inside.
    The label has an optional background rectangle for better visibility.

    Args:
        img: Input image array
        label: Text to display
        bbox: Bounding box coordinates in ``bbox_format`` (default VOC:
            [x_min, y_min, x_max, y_max])
        size: Font size multiplier (default: 1)
        thickness: Text thickness in pixels (default: 2)
        draw_bg: Whether to draw background rectangle (default: True)
        text_bg_color: BGR color tuple for text background (default: white)
        text_color: BGR color tuple for text (default: black)
        top: If True, place label above box; if False, inside (default: True)
        bbox_format: Input bbox format, one of "voc", "coco", "yolo" (default: "voc")

    Returns:
        New image with added label; the input image is not modified

    """
    text_bg_color = _validate_color(text_bg_color)
    text_color = _validate_color(text_color)
    bbox = _check_and_modify_bbox(bbox, img.shape, bbox_format=bbox_format)
    img = img.copy()

    (text_width, text_height), baseline = _get_text_size(label, size, thickness)
    padding = 5  # Padding around text

    bg_width = text_width + 2 * padding
    # Include the font baseline so descenders (p, q, g, ...) stay inside the bg
    bg_height = text_height + baseline + 2 * padding

    # Compare against the full background height so the label only goes above
    # the box when the whole background fits inside the image
    label_above = top and bbox[1] >= bg_height
    bg_x1 = bbox[0]
    bg_y1 = bbox[1] - bg_height if label_above else bbox[1]
    bg_x2 = bg_x1 + bg_width
    bg_y2 = bg_y1 + bg_height

    if draw_bg:
        cv2.rectangle(
            img,
            (bg_x1, bg_y1),
            (bg_x2, bg_y2),
            text_bg_color,
            -1,
        )

    text_x = bg_x1 + padding
    text_y = bg_y1 + padding + text_height  # text baseline; descenders fit below

    cv2.putText(
        img,
        label,
        (text_x, text_y),
        font,
        size,
        text_color,
        thickness,
    )
    return img


def add_multiple_labels(
    img: NDArray[np.uint8],
    labels: list[str],
    bboxes: Sequence[Sequence[float]],
    size: float = 1,
    thickness: int = 2,
    draw_bg: bool = True,
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
    top: bool = True,
    bbox_format: str = "voc",
) -> NDArray[np.uint8]:
    """Add multiple labels to their corresponding bounding boxes using optimized operations.

    Args:
        img: Input image array
        labels: List of text labels
        bboxes: List of bounding boxes, each in ``bbox_format`` (default VOC:
            [x_min, y_min, x_max, y_max])
        size: Font size multiplier (default: 1)
        thickness: Text thickness in pixels (default: 2)
        draw_bg: Whether to draw background rectangles (default: True)
        text_bg_color: BGR color tuple for text backgrounds (default: white)
        text_color: BGR color tuple for text (default: black)
        top: If True, place labels above boxes; if False, inside (default: True)
        bbox_format: Input bbox format, one of "voc", "coco", "yolo" (default: "voc")

    Returns:
        New image with all labels added; the input image is not modified

    """
    # len() instead of truthiness: numpy arrays raise on ambiguous bool()
    if len(bboxes) == 0 or len(labels) == 0:
        raise ValueError("Lists of bounding boxes and labels cannot be empty")
    if len(bboxes) != len(labels):
        raise ValueError("Number of bounding boxes must match number of labels")

    text_bg_color = _validate_color(text_bg_color)
    text_color = _validate_color(text_color)

    # Validate and convert all bboxes to VOC format up front
    converted_bboxes = [
        _check_and_modify_bbox(bbox, img.shape, bbox_format=bbox_format)
        for bbox in bboxes
    ]

    # Draw all labels using add_label (which copies, keeping this function pure)
    output = img
    for label, bbox in zip(labels, converted_bboxes, strict=True):
        output = add_label(
            output,
            label,
            bbox,
            size,
            thickness,
            draw_bg,
            text_bg_color,
            text_color,
            top,
        )
    return output
