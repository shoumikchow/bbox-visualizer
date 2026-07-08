"""Functions for drawing rectangles on images."""

from collections.abc import Sequence

import cv2
import numpy as np
from numpy.typing import NDArray

from ._utils import _check_and_modify_bbox, _validate_color


def draw_rectangle(
    img: NDArray[np.uint8],
    bbox: Sequence[float],
    bbox_color: tuple[int, int, int] = (255, 255, 255),
    thickness: int = 3,
    is_opaque: bool = False,
    alpha: float = 0.5,
    bbox_format: str = "voc",
) -> NDArray[np.uint8]:
    """Draws a rectangle around an object in the image.

    Args:
        img: Input image array
        bbox: Bounding box coordinates in ``bbox_format`` (default VOC:
            [x_min, y_min, x_max, y_max])
        bbox_color: BGR color tuple for the box (default: white)
        thickness: Line thickness in pixels (default: 3)
        is_opaque: If True, draws filled rectangle with transparency (default: False)
        alpha: Transparency level for filled rectangles (default: 0.5)
        bbox_format: Input bbox format, one of "voc", "coco", "yolo" (default: "voc")

    Returns:
        New image with drawn rectangle; the input image is not modified

    """
    _validate_color(bbox_color)
    bbox = _check_and_modify_bbox(bbox, img.shape, bbox_format=bbox_format)

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
    img: NDArray[np.uint8],
    bboxes: Sequence[Sequence[float]],
    bbox_color: tuple[int, int, int] = (255, 255, 255),
    thickness: int = 3,
    is_opaque: bool = False,
    alpha: float = 0.5,
    bbox_format: str = "voc",
) -> NDArray[np.uint8]:
    """Draws multiple rectangles on the image using optimized batched operations.

    Args:
        img: Input image array
        bboxes: List of bounding boxes, each in ``bbox_format`` (default VOC:
            [x_min, y_min, x_max, y_max])
        bbox_color: BGR color tuple for the boxes (default: white)
        thickness: Line thickness in pixels (default: 3)
        is_opaque: If True, draws filled rectangles with transparency (default: False)
        alpha: Transparency level for filled rectangles (default: 0.5)
        bbox_format: Input bbox format, one of "voc", "coco", "yolo" (default: "voc")

    Returns:
        New image with all rectangles drawn; the input image is not modified

    """
    if not bboxes:
        raise ValueError("List of bounding boxes cannot be empty")
    _validate_color(bbox_color)

    # Validate and modify all bboxes
    validated_bboxes = [
        _check_and_modify_bbox(bbox, img.shape, bbox_format=bbox_format)
        for bbox in bboxes
    ]

    output = img.copy()

    if not is_opaque:
        # Convert bboxes to contours for cv2.polylines (draws all rectangles in one call)
        contours = [
            np.array(
                [
                    [bbox[0], bbox[1]],
                    [bbox[2], bbox[1]],
                    [bbox[2], bbox[3]],
                    [bbox[0], bbox[3]],
                ],
                dtype=np.int32,
            )
            for bbox in validated_bboxes
        ]
        cv2.polylines(
            output, contours, isClosed=True, color=bbox_color, thickness=thickness
        )
    else:
        # For opaque rectangles: draw all filled rectangles on one overlay,
        # then do a single alpha blend
        overlay = img.copy()
        for bbox in validated_bboxes:
            cv2.rectangle(
                overlay, (bbox[0], bbox[1]), (bbox[2], bbox[3]), bbox_color, -1
            )
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    return output


# Aliases for preferred naming
draw_box = draw_rectangle
draw_multiple_boxes = draw_multiple_rectangles
