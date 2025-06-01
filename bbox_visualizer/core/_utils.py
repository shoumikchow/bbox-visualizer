"""Internal utilities for bbox-visualizer."""

import logging
from contextlib import contextmanager

# Global flag to track warning suppression state
_warnings_suppressed: bool = False


def suppress_warnings(suppress: bool = True) -> None:
    """Suppress or enable warning messages from bbox-visualizer.

    Args:
        suppress: If True, suppress all warnings. If False, enable warnings.
    """
    global _warnings_suppressed
    _warnings_suppressed = suppress


@contextmanager
def warnings_suppressed():
    """Context manager to temporarily suppress warnings.

    Example:
        >>> with warnings_suppressed():
        ...     # Warnings will be suppressed in this block
        ...     pass
    """
    previous_state = _warnings_suppressed
    suppress_warnings(True)
    try:
        yield
    finally:
        suppress_warnings(previous_state)


def _should_suppress_warning() -> bool:
    """Internal function to check if warnings should be suppressed."""
    return _warnings_suppressed


def _validate_bbox(bbox: list[int]) -> None:
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


def _validate_color(color: tuple[int, int, int]) -> None:
    """Validate BGR color values.

    Args:
        color: BGR color tuple (blue, green, red)

    Raises:
        ValueError: If any color component is outside [0, 255]
    """
    if not all(0 <= c <= 255 for c in color):
        raise ValueError("Color values must be between 0 and 255")


def _check_and_modify_bbox(
    bbox: list[int], img_size: tuple[int, int, int], margin: int = 0
) -> list[int]:
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
