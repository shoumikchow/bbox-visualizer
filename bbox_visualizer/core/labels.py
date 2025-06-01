"""Functions for adding text labels to bounding boxes."""

import cv2
import numpy as np
from numpy.typing import NDArray
from functools import lru_cache

from ._utils import _check_and_modify_bbox, _validate_color

font = cv2.FONT_HERSHEY_SIMPLEX

# Cache text size calculations
@lru_cache(maxsize=128)
def _get_text_size(label: str, size: float, thickness: int) -> tuple[tuple[int, int], int]:
    """Get text size with caching for better performance."""
    return cv2.getTextSize(label, font, size, thickness)


def add_label(
    img: NDArray[np.uint8],
    label: str,
    bbox: list[int],
    size: float = 1,
    thickness: int = 2,
    draw_bg: bool = True,
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
    top: bool = True,
) -> NDArray[np.uint8]:
    """Add a label to a bounding box, either above or inside it.

    If there isn't enough space above the box, the label is placed inside.
    The label has an optional background rectangle for better visibility.

    Args:
        img: Input image array
        label: Text to display
        bbox: List of [x_min, y_min, x_max, y_max] coordinates
        size: Font size multiplier (default: 1)
        thickness: Text thickness in pixels (default: 2)
        draw_bg: Whether to draw background rectangle (default: True)
        text_bg_color: BGR color tuple for text background (default: white)
        text_color: BGR color tuple for text (default: black)
        top: If True, place label above box; if False, inside (default: True)

    Returns:
        Image with added label

    """
    _validate_color(text_bg_color)
    _validate_color(text_color)
    bbox = _check_and_modify_bbox(bbox, img.shape)

    # Use cached text size calculation
    (text_width, text_height), baseline = _get_text_size(label, size, thickness)
    padding = 5  # Padding around text

    if top and bbox[1] - text_height > text_height:
        # Calculate background rectangle dimensions
        bg_width = text_width + 2 * padding
        bg_height = text_height + 2 * padding

        # Calculate background rectangle position
        bg_x1 = bbox[0]
        bg_y1 = bbox[1] - bg_height
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

        # Center text in background rectangle
        text_x = bg_x1 + (bg_width - text_width) // 2
        text_y = bg_y1 + (bg_height + text_height) // 2

        cv2.putText(
            img,
            label,
            (text_x, text_y),
            font,
            size,
            text_color,
            thickness,
        )
    else:
        # Calculate background rectangle dimensions
        bg_width = text_width + 2 * padding
        bg_height = text_height + 2 * padding

        # Calculate background rectangle position
        bg_x1 = bbox[0]
        bg_y1 = bbox[1]
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

        # Center text in background rectangle
        text_x = bg_x1 + (bg_width - text_width) // 2
        text_y = bg_y1 + (bg_height + text_height) // 2

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
    bboxes: list[list[int]],
    size: float = 1,
    thickness: int = 2,
    draw_bg: bool = True,
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
    top: bool = True,
) -> NDArray[np.uint8]:
    """Add multiple labels to their corresponding bounding boxes using optimized operations.

    Args:
        img: Input image array
        labels: List of text labels
        bboxes: List of bounding boxes, each containing [x_min, y_min, x_max, y_max]
        size: Font size multiplier (default: 1)
        thickness: Text thickness in pixels (default: 2)
        draw_bg: Whether to draw background rectangles (default: True)
        text_bg_color: BGR color tuple for text backgrounds (default: white)
        text_color: BGR color tuple for text (default: black)
        top: If True, place labels above boxes; if False, inside (default: True)

    Returns:
        Image with all labels added

    """
    if not bboxes or not labels:
        raise ValueError("Lists of bounding boxes and labels cannot be empty")
    if len(bboxes) != len(labels):
        raise ValueError("Number of bounding boxes must match number of labels")

    _validate_color(text_bg_color)
    _validate_color(text_color)
    
    # Convert bboxes to numpy array for vectorized operations
    bboxes = np.array(bboxes)
    
    # Validate and modify all bboxes at once
    bboxes = np.array([_check_and_modify_bbox(bbox, img.shape) for bbox in bboxes])
    
    # Draw all labels using add_label
    output = img.copy()
    for label, bbox in zip(labels, bboxes):
        output = add_label(
            output,
            label,
            bbox.tolist(),
            size,
            thickness,
            draw_bg,
            text_bg_color,
            text_color,
            top
        )
    return output
