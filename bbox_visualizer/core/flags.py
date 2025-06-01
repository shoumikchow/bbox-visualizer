"""Functions for drawing flag and T-shaped labels."""

import logging

import cv2
import numpy as np
from numpy.typing import NDArray

from ._utils import _check_and_modify_bbox, _should_suppress_warning, _validate_color
from .labels import add_label
from .rectangle import draw_rectangle

font = cv2.FONT_HERSHEY_SIMPLEX


def add_T_label(
    img: NDArray[np.uint8],
    label: str,
    bbox: list[int],
    size: float = 1,
    thickness: int = 2,
    draw_bg: bool = True,
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
) -> NDArray[np.uint8]:
    """Add a T-shaped label with a vertical line connecting to the bounding box.

    The label consists of a vertical line extending from the top of the box
    and a horizontal label at the top. Falls back to regular label if there isn't
    enough space above the box.

    Args:
        img: Input image array
        label: Text to display
        bbox: List of [x_min, y_min, x_max, y_max] coordinates
        size: Font size multiplier (default: 1)
        thickness: Text thickness in pixels (default: 2)
        draw_bg: Whether to draw background rectangle (default: True)
        text_bg_color: BGR color tuple for text background (default: white)
        text_color: BGR color tuple for text (default: black)

    Returns:
        Image with added T-shaped label

    """
    _validate_color(text_bg_color)
    _validate_color(text_color)
    bbox = _check_and_modify_bbox(bbox, img.shape)
    (label_width, label_height), baseline = cv2.getTextSize(
        label, font, size, thickness
    )
    padding = 5  # Padding around text

    # draw vertical line
    x_center = (bbox[0] + bbox[2]) // 2
    line_top = y_top = bbox[1] - 50

    # draw rectangle with label
    y_bottom = y_top
    y_top = y_bottom - label_height - 2 * padding

    if y_top < 0:
        if not _should_suppress_warning():
            logging.warning(
                "Labelling style 'T' going out of frame. Falling back to normal labeling."
            )
        return add_label(img, label, bbox)

    cv2.line(img, (x_center, bbox[1]), (x_center, line_top), text_bg_color, 3)

    # Calculate background rectangle dimensions
    bg_width = label_width + 2 * padding
    bg_height = label_height + 2 * padding

    # Calculate background rectangle position
    bg_x1 = x_center - (bg_width // 2)
    bg_y1 = y_top
    bg_x2 = bg_x1 + bg_width
    bg_y2 = bg_y1 + bg_height

    if draw_bg:
        cv2.rectangle(img, (bg_x1, bg_y1), (bg_x2, bg_y2), text_bg_color, -1)

    # Center text in background rectangle
    text_x = bg_x1 + (bg_width - label_width) // 2
    text_y = bg_y1 + (bg_height + label_height) // 2

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


def draw_flag_with_label(
    img: NDArray[np.uint8],
    label: str,
    bbox: list[int],
    size: float = 1,
    thickness: int = 2,
    write_label: bool = True,
    line_color: tuple[int, int, int] = (255, 255, 255),
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
) -> NDArray[np.uint8]:
    """Draws a flag-like label with a vertical line and text box.

    The flag consists of a vertical line extending from the middle of the box
    and a horizontal label at the top. Falls back to regular label if there isn't
    enough space above the box.

    Args:
        img: Input image array
        label: Text to display
        bbox: List of [x_min, y_min, x_max, y_max] coordinates
        size: Font size multiplier (default: 1)
        thickness: Text thickness in pixels (default: 2)
        write_label: Whether to draw the text label (default: True)
        line_color: BGR color tuple for the vertical line (default: white)
        text_bg_color: BGR color tuple for text background (default: white)
        text_color: BGR color tuple for text (default: black)

    Returns:
        Image with added flag label

    """
    _validate_color(line_color)
    _validate_color(text_bg_color)
    _validate_color(text_color)
    bbox = _check_and_modify_bbox(bbox, img.shape)
    (label_width, label_height), baseline = cv2.getTextSize(
        label, font, size, thickness
    )

    x_center = (bbox[0] + bbox[2]) // 2
    y_bottom = int(bbox[1] * 0.75 + bbox[3] * 0.25)
    y_top = bbox[1] - (y_bottom - bbox[1])
    if y_top < 0:
        if not _should_suppress_warning():
            logging.warning(
                "Labelling style 'Flag' going out of frame. Falling back to normal labeling."
            )
        img = draw_rectangle(img, bbox, bbox_color=line_color)
        return add_label(img, label, bbox)

    start_point = (x_center, y_top)
    end_point = (x_center, y_bottom)

    cv2.line(img, start_point, end_point, line_color, 3)

    # write label
    if write_label:
        text_width = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0][0]
        label_bg = [
            start_point[0],
            start_point[1],
            start_point[0] + text_width,
            start_point[1] + 30,
        ]
        cv2.rectangle(
            img,
            (label_bg[0], label_bg[1]),
            (label_bg[2] + 5, label_bg[3]),
            text_bg_color,
            -1,
        )
        cv2.putText(
            img,
            label,
            (start_point[0] + 5, start_point[1] - 5 + 30),
            font,
            size,
            text_color,
            thickness,
        )

    return img


def add_multiple_T_labels(
    img: NDArray[np.uint8],
    labels: list[str],
    bboxes: list[list[int]],
    draw_bg: bool = True,
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
) -> NDArray[np.uint8]:
    """Add multiple T-shaped labels to their corresponding bounding boxes.

    Args:
        img: Input image array
        labels: List of text labels
        bboxes: List of bounding boxes, each containing [x_min, y_min, x_max, y_max]
        draw_bg: Whether to draw background rectangles (default: True)
        text_bg_color: BGR color tuple for text backgrounds (default: white)
        text_color: BGR color tuple for text (default: black)

    Returns:
        Image with all T-shaped labels added

    """
    if not bboxes or not labels:
        raise ValueError("Lists of bounding boxes and labels cannot be empty")
    if len(bboxes) != len(labels):
        raise ValueError("Number of bounding boxes must match number of labels")

    _validate_color(text_bg_color)
    _validate_color(text_color)
    for label, bbox in zip(labels, bboxes):
        img = add_T_label(
            img,
            label,
            bbox,
            size=1,
            thickness=2,
            draw_bg=draw_bg,
            text_bg_color=text_bg_color,
            text_color=text_color,
        )

    return img


def draw_multiple_flags_with_labels(
    img: NDArray[np.uint8],
    labels: list[str],
    bboxes: list[list[int]],
    write_label: bool = True,
    line_color: tuple[int, int, int] = (255, 255, 255),
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
) -> NDArray[np.uint8]:
    """Add multiple flag-like labels to their corresponding bounding boxes.

    Args:
        img: Input image array
        labels: List of text labels
        bboxes: List of bounding boxes, each containing [x_min, y_min, x_max, y_max]
        write_label: Whether to draw the text labels (default: True)
        line_color: BGR color tuple for the vertical lines (default: white)
        text_bg_color: BGR color tuple for text backgrounds (default: white)
        text_color: BGR color tuple for text (default: black)

    Returns:
        Image with all flag labels added

    """
    if not bboxes or not labels:
        raise ValueError("Lists of bounding boxes and labels cannot be empty")
    if len(bboxes) != len(labels):
        raise ValueError("Number of bounding boxes must match number of labels")

    _validate_color(line_color)
    _validate_color(text_bg_color)
    _validate_color(text_color)
    for label, bbox in zip(labels, bboxes):
        img = draw_flag_with_label(
            img,
            label,
            bbox,
            size=1,
            thickness=2,
            write_label=write_label,
            line_color=line_color,
            text_bg_color=text_bg_color,
            text_color=text_color,
        )

    return img
