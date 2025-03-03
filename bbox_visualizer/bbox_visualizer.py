import cv2
import logging
from typing import List, Tuple
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX


def check_and_modify_bbox(
    bbox: List[int], img_size: Tuple[int, int, int], margin: int = 0
) -> List[int]:
    """Checks and adjusts bounding box coordinates to fit within image boundaries.

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
    bbox = [value if value > 0 else margin for value in bbox]
    bbox[2] = bbox[2] if bbox[2] < img_size[1] else img_size[1] - margin
    bbox[3] = bbox[3] if bbox[3] < img_size[0] else img_size[0] - margin
    return bbox


def draw_rectangle(
    img: np.ndarray,
    bbox: List[int],
    bbox_color: Tuple[int, int, int] = (255, 255, 255),
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
    bbox = check_and_modify_bbox(bbox, img.shape)

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


def add_label(
    img: np.ndarray,
    label: str,
    bbox: List[int],
    size: float = 1,
    thickness: int = 2,
    draw_bg: bool = True,
    text_bg_color: Tuple[int, int, int] = (255, 255, 255),
    text_color: Tuple[int, int, int] = (0, 0, 0),
    top: bool = True,
) -> np.ndarray:
    """Adds a label to a bounding box, either above or inside it.

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
    (text_width, text_height), baseline = cv2.getTextSize(label, font, size, thickness)
    padding = 5  # Padding around text

    if top and bbox[1] - text_height > text_height:
        # Calculate background rectangle dimensions
        bg_width = text_width + 2 * padding
        bg_height = text_height + 2 * padding

        # Calculate background rectangle position
        bg_x1 = bbox[0]
        bg_y1 = bbox[1] - bg_height  # Removed the gap by removing (5 * size)
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


def add_T_label(
    img: np.ndarray,
    label: str,
    bbox: List[int],
    size: float = 1,
    thickness: int = 2,
    draw_bg: bool = True,
    text_bg_color: Tuple[int, int, int] = (255, 255, 255),
    text_color: Tuple[int, int, int] = (0, 0, 0),
) -> np.ndarray:
    """Adds a T-shaped label with a vertical line connecting to the bounding box.

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
    img: np.ndarray,
    label: str,
    bbox: List[int],
    size: float = 1,
    thickness: int = 2,
    write_label: bool = True,
    line_color: Tuple[int, int, int] = (255, 255, 255),
    text_bg_color: Tuple[int, int, int] = (255, 255, 255),
    text_color: Tuple[int, int, int] = (0, 0, 0),
) -> np.ndarray:
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
    # draw vertical line
    (label_width, label_height), baseline = cv2.getTextSize(
        label, font, size, thickness
    )

    x_center = (bbox[0] + bbox[2]) // 2
    y_bottom = int((bbox[1] * 0.75 + bbox[3] * 0.25))
    y_top = bbox[1] - (y_bottom - bbox[1])
    if y_top < 0:
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


def draw_multiple_rectangles(
    img: np.ndarray,
    bboxes: List[List[int]],
    bbox_color: Tuple[int, int, int] = (255, 255, 255),
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
    for bbox in bboxes:
        img = draw_rectangle(img, bbox, bbox_color, thickness, is_opaque, alpha)
    return img


def add_multiple_labels(
    img: np.ndarray,
    labels: List[str],
    bboxes: List[List[int]],
    size: float = 1,
    thickness: int = 2,
    draw_bg: bool = True,
    text_bg_color: Tuple[int, int, int] = (255, 255, 255),
    text_color: Tuple[int, int, int] = (0, 0, 0),
    top: bool = True,
) -> np.ndarray:
    """Adds multiple labels to their corresponding bounding boxes.

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
    for label, bbox in zip(labels, bboxes):
        img = add_label(
            img, label, bbox, size, thickness, draw_bg, text_bg_color, text_color, top
        )
    return img


def add_multiple_T_labels(
    img: np.ndarray,
    labels: List[str],
    bboxes: List[List[int]],
    draw_bg: bool = True,
    text_bg_color: Tuple[int, int, int] = (255, 255, 255),
    text_color: Tuple[int, int, int] = (0, 0, 0),
) -> np.ndarray:
    """Adds multiple T-shaped labels to their corresponding bounding boxes.

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
    img: np.ndarray,
    labels: List[str],
    bboxes: List[List[int]],
    write_label: bool = True,
    line_color: Tuple[int, int, int] = (255, 255, 255),
    text_bg_color: Tuple[int, int, int] = (255, 255, 255),
    text_color: Tuple[int, int, int] = (0, 0, 0),
) -> np.ndarray:
    """Adds multiple flag-like labels to their corresponding bounding boxes.

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
