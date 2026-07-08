"""Functions for drawing rectangles on images."""

from collections.abc import Sequence
from typing import cast

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
        # Shift the stroke inward so its outer edge lies on the bbox coordinates
        # (cv2 centers the stroke on the coords, spilling outside the box and
        # misaligning with labels drawn flush at bbox[0]). cv2's measured stroke
        # half-width is (t+1)//2 for t > 1, not t//2.
        shift = (thickness + 1) // 2 if thickness > 1 else 0
        cv2.rectangle(
            output,
            (bbox[0] + shift, bbox[1] + shift),
            (bbox[2] - shift, bbox[3] - shift),
            bbox_color,
            thickness,
        )
    else:
        overlay = img.copy()
        cv2.rectangle(overlay, (bbox[0], bbox[1]), (bbox[2], bbox[3]), bbox_color, -1)
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    return output


def draw_multiple_rectangles(
    img: NDArray[np.uint8],
    bboxes: Sequence[Sequence[float]],
    bbox_color: tuple[int, int, int] | Sequence[tuple[int, int, int]] = (
        255,
        255,
        255,
    ),
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
        bbox_color: BGR color tuple applied to all boxes, or a sequence of
            one color per box (default: white)
        thickness: Line thickness in pixels (default: 3)
        is_opaque: If True, draws filled rectangles with transparency (default: False)
        alpha: Transparency level for filled rectangles (default: 0.5)
        bbox_format: Input bbox format, one of "voc", "coco", "yolo" (default: "voc")

    Returns:
        New image with all rectangles drawn; the input image is not modified

    """
    if not bboxes:
        raise ValueError("List of bounding boxes cannot be empty")

    per_box_colors = len(bbox_color) > 0 and isinstance(bbox_color[0], (tuple, list))
    colors: list[tuple[int, int, int]]
    if per_box_colors:
        if len(bbox_color) != len(bboxes):
            raise ValueError(
                f"Number of colors ({len(bbox_color)}) must match "
                f"number of bounding boxes ({len(bboxes)})"
            )
        color_seq = cast("Sequence[tuple[int, int, int]]", bbox_color)
        colors = [tuple(color) for color in color_seq]
    else:
        colors = [cast("tuple[int, int, int]", bbox_color)] * len(bboxes)
    for color in colors:
        _validate_color(color)

    # Validate and modify all bboxes
    validated_bboxes = [
        _check_and_modify_bbox(bbox, img.shape, bbox_format=bbox_format)
        for bbox in bboxes
    ]

    output = img.copy()

    if not is_opaque:
        # Shift the stroke inward so its outer edge lies on the bbox coordinates,
        # matching draw_rectangle
        shift = (thickness + 1) // 2 if thickness > 1 else 0
        if per_box_colors:
            # cv2.polylines batches only a single color, so draw box by box
            for bbox, color in zip(validated_bboxes, colors):
                cv2.rectangle(
                    output,
                    (bbox[0] + shift, bbox[1] + shift),
                    (bbox[2] - shift, bbox[3] - shift),
                    color,
                    thickness,
                )
        else:
            # Convert bboxes to contours for cv2.polylines
            # (draws all rectangles in one call)
            contours = [
                np.array(
                    [
                        [bbox[0] + shift, bbox[1] + shift],
                        [bbox[2] - shift, bbox[1] + shift],
                        [bbox[2] - shift, bbox[3] - shift],
                        [bbox[0] + shift, bbox[3] - shift],
                    ],
                    dtype=np.int32,
                )
                for bbox in validated_bboxes
            ]
            cv2.polylines(
                output, contours, isClosed=True, color=colors[0], thickness=thickness
            )
    else:
        # For opaque rectangles: draw all filled rectangles on one overlay,
        # then do a single alpha blend
        overlay = img.copy()
        for bbox, color in zip(validated_bboxes, colors):
            cv2.rectangle(overlay, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, -1)
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    return output


# Aliases for preferred naming
draw_box = draw_rectangle
draw_multiple_boxes = draw_multiple_rectangles
