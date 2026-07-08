"""Internal utilities for bbox-visualizer."""

import numbers
from collections.abc import Sequence
from functools import lru_cache

import cv2

#: Bounding box formats accepted by the public API.
SUPPORTED_BBOX_FORMATS = ("voc", "coco", "yolo")


@lru_cache(maxsize=128)
def _get_text_size(
    label: str, size: float, thickness: int
) -> tuple[Sequence[int], int]:
    """Get text size with caching for better performance."""
    return cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, size, thickness)


def _validate_bbox(bbox: list[int]) -> None:
    """Validate bounding box format and values.

    Args:
        bbox: List of [x_min, y_min, x_max, y_max] coordinates

    Raises:
        ValueError: If bbox is empty, has wrong length, or has invalid coordinates

    """
    if bbox is None or (hasattr(bbox, "__len__") and len(bbox) == 0):
        raise ValueError("Bounding box cannot be empty")
    if len(bbox) != 4:
        raise ValueError(
            "Bounding box must have exactly 4 coordinates [x_min, y_min, x_max, y_max]"
        )
    if bbox[0] > bbox[2] or bbox[1] > bbox[3]:
        raise ValueError(
            "Invalid bounding box coordinates: x_min > x_max or y_min > y_max"
        )


def _validate_color(color: Sequence[int]) -> tuple[int, int, int]:
    """Validate a BGR color sequence and normalize it to a tuple of ints.

    Args:
        color: BGR color sequence to validate

    Returns:
        The color as a tuple of built-in ints (cv2 rejects numpy scalars)

    Raises:
        ValueError: If color is not a valid BGR sequence

    """
    if not hasattr(color, "__len__") or len(color) != 3:
        raise ValueError("Color must be a sequence of 3 integers (BGR)")
    # numbers.Integral also admits numpy integer scalars, e.g. colors
    # sampled from image pixels (np.uint8)
    if not all(isinstance(c, numbers.Integral) and 0 <= c <= 255 for c in color):
        raise ValueError("Color values must be integers between 0 and 255")
    b, g, r = (int(c) for c in color)
    return (b, g, r)


def _convert_bbox_to_voc(
    bbox: Sequence[float],
    img_size: tuple[int, ...],
    bbox_format: str = "voc",
) -> list[int]:
    """Convert a bounding box from the given format to Pascal VOC format.

    Supported input formats:
        - ``"voc"``:  ``[x_min, y_min, x_max, y_max]`` in absolute pixels (default)
        - ``"coco"``: ``[x_min, y_min, width, height]`` in absolute pixels
        - ``"yolo"``: ``[x_center, y_center, width, height]`` normalized to ``[0, 1]``

    Args:
        bbox: Bounding box coordinates expressed in ``bbox_format``
        img_size: Tuple of (height, width, channels); used to denormalize YOLO boxes
        bbox_format: One of ``"voc"``, ``"coco"``, or ``"yolo"`` (default: ``"voc"``)

    Returns:
        Bounding box as ``[x_min, y_min, x_max, y_max]`` in absolute integer pixels

    Raises:
        ValueError: If ``bbox_format`` is unsupported or ``bbox`` is not 4 values

    """
    fmt = bbox_format.lower()
    if fmt not in SUPPORTED_BBOX_FORMATS:
        raise ValueError(
            f"Unsupported bbox_format {bbox_format!r}. "
            f"Expected one of {SUPPORTED_BBOX_FORMATS}."
        )
    if bbox is None or len(bbox) != 4:
        raise ValueError("Bounding box must have exactly 4 coordinates")

    if fmt == "voc":
        x_min, y_min, x_max, y_max = bbox
    elif fmt == "coco":
        x_min, y_min, width, height = bbox
        if width < 0 or height < 0:
            raise ValueError("COCO bounding box width and height must be non-negative")
        x_max, y_max = x_min + width, y_min + height
    else:  # yolo
        img_height, img_width = img_size[0], img_size[1]
        x_center, y_center, width, height = bbox
        if width < 0 or height < 0:
            raise ValueError("YOLO bounding box width and height must be non-negative")
        x_min = (x_center - width / 2) * img_width
        y_min = (y_center - height / 2) * img_height
        x_max = (x_center + width / 2) * img_width
        y_max = (y_center + height / 2) * img_height

    return [round(x_min), round(y_min), round(x_max), round(y_max)]


def _check_and_modify_bbox(
    bbox: Sequence[float],
    img_size: tuple[int, ...],
    margin: int = 0,
    bbox_format: str = "voc",
) -> list[int]:
    """Check and adjust bounding box coordinates.

    .. private::

    Trimming rules:
        - xmin/ymin: Set to margin if negative
        - xmax/ymax: Set to image width/height - margin if exceeds image size

    Args:
        bbox: Bounding box coordinates expressed in ``bbox_format``
        img_size: Tuple of (height, width, channels)
        margin: Minimum distance from image edges (default: 0)
        bbox_format: Input format, one of "voc", "coco", "yolo" (default: "voc")

    Returns:
        Adjusted bounding box coordinates [x_min, y_min, x_max, y_max]

    """
    bbox = _convert_bbox_to_voc(bbox, img_size, bbox_format)
    _validate_bbox(bbox)
    bbox = [value if value > 0 else margin for value in bbox]
    bbox[2] = bbox[2] if bbox[2] < img_size[1] else img_size[1] - margin
    bbox[3] = bbox[3] if bbox[3] < img_size[0] else img_size[0] - margin
    return bbox
