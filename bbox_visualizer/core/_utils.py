"""Internal utilities for bbox-visualizer."""

from typing import List, Tuple


def _validate_bbox(bbox: List[int]) -> None:
    """Validate bounding box format and values.

    Args:
        bbox: List of [x_min, y_min, x_max, y_max] coordinates

    Raises:
        ValueError: If bbox is empty, has wrong length, or has invalid coordinates
    """
    if not bbox:
        raise ValueError("Bounding box cannot be empty")
    if len(bbox) != 4:
        raise ValueError(
            "Bounding box must have exactly 4 coordinates [x_min, y_min, x_max, y_max]"
        )
    if bbox[0] > bbox[2] or bbox[1] > bbox[3]:
        raise ValueError(
            "Invalid bounding box coordinates: x_min > x_max or y_min > y_max"
        )


def _validate_color(color: Tuple[int, int, int]) -> None:
    """Validate BGR color values.

    Args:
        color: BGR color tuple (blue, green, red)

    Raises:
        ValueError: If any color component is outside [0, 255]
    """
    if not all(0 <= c <= 255 for c in color):
        raise ValueError("Color values must be between 0 and 255")


def _check_and_modify_bbox(
    bbox: List[int], img_size: Tuple[int, int, int], margin: int = 0
) -> List[int]:
    """Internal function to check and adjust bounding box coordinates.

    .. private::

    Trimming rules:
        - xmin/ymin: Set to margin if negative
        - xmax/ymax: Set to image width/height - margin if exceeds image size

    Args:
        bbox: List of [x_min, y_min, x_max, y_max] coordinates
        img_size: Tuple of (height, width, channels)
        margin: Minimum distance from image edges (default: 0)

    Returns:
        Adjusted bounding box coordinates [x_min, y_min, x_max, y_max]
    """
    _validate_bbox(bbox)
    bbox = [value if value > 0 else margin for value in bbox]
    bbox[2] = bbox[2] if bbox[2] < img_size[1] else img_size[1] - margin
    bbox[3] = bbox[3] if bbox[3] < img_size[0] else img_size[0] - margin
    return bbox
