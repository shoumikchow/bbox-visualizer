"""Functions for drawing flag and T-shaped labels."""

import logging
from collections.abc import Sequence

import cv2
import numpy as np
from numpy.typing import NDArray

from ._utils import _check_and_modify_bbox, _get_ink_metrics, _validate_color
from .labels import add_label
from .rectangle import draw_rectangle

logger = logging.getLogger(__name__)

font = cv2.FONT_HERSHEY_SIMPLEX

#: Length in pixels of the vertical line connecting a T label to its box.
T_LINE_LENGTH = 50


def add_T_label(
    img: NDArray[np.uint8],
    label: str,
    bbox: Sequence[float],
    size: float = 1,
    thickness: int = 2,
    draw_bg: bool = True,
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
    bbox_format: str = "voc",
) -> NDArray[np.uint8]:
    """Add a T-shaped label with a vertical line connecting to the bounding box.

    The label consists of a vertical line extending from the top of the box
    and a horizontal label at the top. Falls back to regular label if there isn't
    enough space above the box.

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
        bbox_format: Input bbox format, one of "voc", "coco", "yolo" (default: "voc")

    Returns:
        New image with added T-shaped label; the input image is not modified

    """
    text_bg_color = _validate_color(text_bg_color)
    text_color = _validate_color(text_color)
    bbox = _check_and_modify_bbox(bbox, img.shape, bbox_format=bbox_format)
    img = img.copy()
    label_width, ascent, descent = _get_ink_metrics(label, size, thickness)
    padding = 5  # Padding around text

    # draw vertical line
    x_center = (bbox[0] + bbox[2]) // 2
    line_top = y_top = bbox[1] - T_LINE_LENGTH

    # draw rectangle with label
    y_bottom = y_top
    y_top = y_bottom - (ascent + descent + 2 * padding)

    if y_top < 0:
        logger.warning(
            "Labelling style 'T' going out of frame. Falling back to normal labeling."
        )
        return add_label(
            img,
            label,
            bbox,
            size=size,
            thickness=thickness,
            draw_bg=draw_bg,
            text_bg_color=text_bg_color,
            text_color=text_color,
        )

    cv2.line(img, (x_center, bbox[1]), (x_center, line_top), text_bg_color, 3)

    # Calculate background rectangle dimensions
    bg_width = label_width + 2 * padding
    # Size the bg from measured ink so it hugs the text on all sides
    bg_height = ascent + descent + 2 * padding

    # Calculate background rectangle position
    bg_x1 = x_center - (bg_width // 2)
    bg_y1 = y_top
    bg_x2 = bg_x1 + bg_width
    bg_y2 = bg_y1 + bg_height

    if draw_bg:
        cv2.rectangle(img, (bg_x1, bg_y1), (bg_x2, bg_y2), text_bg_color, -1)

    text_x = bg_x1 + padding
    text_y = bg_y1 + padding + ascent  # text baseline; descenders fit below

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
    bbox: Sequence[float],
    size: float = 1,
    thickness: int = 2,
    write_label: bool = True,
    line_color: tuple[int, int, int] = (255, 255, 255),
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
    bbox_format: str = "voc",
) -> NDArray[np.uint8]:
    """Draws a flag-like label with a vertical line and text box.

    The flag consists of a vertical line extending from the middle of the box
    and a horizontal label at the top. Falls back to regular label if there isn't
    enough space above the box.

    Args:
        img: Input image array
        label: Text to display
        bbox: Bounding box coordinates in ``bbox_format`` (default VOC:
            [x_min, y_min, x_max, y_max])
        size: Font size multiplier (default: 1)
        thickness: Text thickness in pixels (default: 2)
        write_label: Whether to draw the text label (default: True)
        line_color: BGR color tuple for the vertical line (default: white)
        text_bg_color: BGR color tuple for text background (default: white)
        text_color: BGR color tuple for text (default: black)
        bbox_format: Input bbox format, one of "voc", "coco", "yolo" (default: "voc")

    Returns:
        New image with added flag label; the input image is not modified

    """
    line_color = _validate_color(line_color)
    text_bg_color = _validate_color(text_bg_color)
    text_color = _validate_color(text_color)
    bbox = _check_and_modify_bbox(bbox, img.shape, bbox_format=bbox_format)
    img = img.copy()
    label_width, ascent, descent = _get_ink_metrics(label, size, thickness)

    x_center = (bbox[0] + bbox[2]) // 2
    y_bottom = int(bbox[1] * 0.75 + bbox[3] * 0.25)
    # Rise height/4 above the box, but at least T_LINE_LENGTH so the pole
    # stays visible on small boxes
    y_top = bbox[1] - max(y_bottom - bbox[1], T_LINE_LENGTH)
    if y_top < 0:
        logger.warning(
            "Labelling style 'Flag' going out of frame. Falling back to normal labeling."
        )
        img = draw_rectangle(img, bbox, bbox_color=line_color)
        return add_label(
            img,
            label,
            bbox,
            size=size,
            thickness=thickness,
            text_bg_color=text_bg_color,
            text_color=text_color,
        )

    start_point = (x_center, y_top)
    end_point = (x_center, y_bottom)

    # Start the pole 2px below the flag top: cv2 caps the 3px stroke ~2px
    # past the endpoint, which would poke above the flag background
    cv2.line(img, (x_center, y_top + 2), end_point, line_color, 3)

    # write label
    if write_label:
        padding = 5  # Padding around text
        bg_x2 = start_point[0] + label_width + 2 * padding
        # Size the bg from measured ink so it hugs the text on all sides
        bg_y2 = start_point[1] + ascent + descent + 2 * padding
        cv2.rectangle(img, start_point, (bg_x2, bg_y2), text_bg_color, -1)
        cv2.putText(
            img,
            label,
            (start_point[0] + padding, start_point[1] + padding + ascent),
            font,
            size,
            text_color,
            thickness,
        )

    return img


def add_multiple_T_labels(
    img: NDArray[np.uint8],
    labels: list[str],
    bboxes: Sequence[Sequence[float]],
    draw_bg: bool = True,
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
    bbox_format: str = "voc",
) -> NDArray[np.uint8]:
    """Add multiple T-shaped labels to their corresponding bounding boxes.

    Args:
        img: Input image array
        labels: List of text labels
        bboxes: List of bounding boxes, each in ``bbox_format`` (default VOC:
            [x_min, y_min, x_max, y_max])
        draw_bg: Whether to draw background rectangles (default: True)
        text_bg_color: BGR color tuple for text backgrounds (default: white)
        text_color: BGR color tuple for text (default: black)
        bbox_format: Input bbox format, one of "voc", "coco", "yolo" (default: "voc")

    Returns:
        New image with all T-shaped labels added; the input image is not modified

    """
    # len() instead of truthiness: numpy arrays raise on ambiguous bool()
    if bboxes is None or labels is None or len(bboxes) == 0 or len(labels) == 0:
        raise ValueError("Lists of bounding boxes and labels cannot be empty")
    if len(bboxes) != len(labels):
        raise ValueError("Number of bounding boxes must match number of labels")

    text_bg_color = _validate_color(text_bg_color)
    text_color = _validate_color(text_color)
    for label, bbox in zip(labels, bboxes, strict=True):
        img = add_T_label(
            img,
            label,
            bbox,
            size=1,
            thickness=2,
            draw_bg=draw_bg,
            text_bg_color=text_bg_color,
            text_color=text_color,
            bbox_format=bbox_format,
        )

    return img


def draw_multiple_flags_with_labels(
    img: NDArray[np.uint8],
    labels: list[str],
    bboxes: Sequence[Sequence[float]],
    write_label: bool = True,
    line_color: tuple[int, int, int] = (255, 255, 255),
    text_bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
    bbox_format: str = "voc",
) -> NDArray[np.uint8]:
    """Add multiple flag-like labels to their corresponding bounding boxes.

    Args:
        img: Input image array
        labels: List of text labels
        bboxes: List of bounding boxes, each in ``bbox_format`` (default VOC:
            [x_min, y_min, x_max, y_max])
        write_label: Whether to draw the text labels (default: True)
        line_color: BGR color tuple for the vertical lines (default: white)
        text_bg_color: BGR color tuple for text backgrounds (default: white)
        text_color: BGR color tuple for text (default: black)
        bbox_format: Input bbox format, one of "voc", "coco", "yolo" (default: "voc")

    Returns:
        New image with all flag labels added; the input image is not modified

    """
    # len() instead of truthiness: numpy arrays raise on ambiguous bool()
    if bboxes is None or labels is None or len(bboxes) == 0 or len(labels) == 0:
        raise ValueError("Lists of bounding boxes and labels cannot be empty")
    if len(bboxes) != len(labels):
        raise ValueError("Number of bounding boxes must match number of labels")

    line_color = _validate_color(line_color)
    text_bg_color = _validate_color(text_bg_color)
    text_color = _validate_color(text_color)
    for label, bbox in zip(labels, bboxes, strict=True):
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
            bbox_format=bbox_format,
        )

    return img
