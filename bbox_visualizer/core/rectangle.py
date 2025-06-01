"""Functions for drawing rectangles on images."""

import cv2
import numpy as np

from ._utils import _check_and_modify_bbox, _validate_color


def draw_rectangle(
    img: np.ndarray,
    bbox: list[int],
    bbox_color: tuple[int, int, int] = (255, 255, 255),
    thickness: int = 3,
    is_opaque: bool = False,
    alpha: float = 0.5,
) -> np.ndarray:
    """Draws a rectangle around an object in the image.

    Args:
        img: Input image array
        bbox: List of [x_min, y_min, x_max, y_max] coordinates
        bbox_color: BGR color tuple for the box (default: white)
        thickness: Line thickness in pixels (default: 3)
        is_opaque: If True, draws filled rectangle with transparency (default: False)
        alpha: Transparency level for filled rectangles (default: 0.5)

    Returns:
        Image with drawn rectangle
    """
    _validate_color(bbox_color)
    bbox = _check_and_modify_bbox(bbox, img.shape)

    output = img.copy()
    if not is_opaque:
        cv2.rectangle(
            output, (bbox[0], bbox[1]), (bbox[2], bbox[3]), bbox_color, thickness
        )
    else:
        overlay = img.copy()
        cv2.rectangle(overlay, (bbox[0], bbox[1]), (bbox[2], bbox[3]), bbox_color, -1)
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    return output


def draw_multiple_rectangles(
    img: np.ndarray,
    bboxes: list[list[int]],
    bbox_color: tuple[int, int, int] = (255, 255, 255),
    thickness: int = 3,
    is_opaque: bool = False,
    alpha: float = 0.5,
) -> np.ndarray:
    """Draws multiple rectangles on the image.

    Args:
        img: Input image array
        bboxes: List of bounding boxes, each containing [x_min, y_min, x_max, y_max]
        bbox_color: BGR color tuple for the boxes (default: white)
        thickness: Line thickness in pixels (default: 3)
        is_opaque: If True, draws filled rectangles with transparency (default: False)
        alpha: Transparency level for filled rectangles (default: 0.5)

    Returns:
        Image with all rectangles drawn
    """
    if not bboxes:
        raise ValueError("List of bounding boxes cannot be empty")
    _validate_color(bbox_color)
    for bbox in bboxes:
        img = draw_rectangle(img, bbox, bbox_color, thickness, is_opaque, alpha)
    return img
