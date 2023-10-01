import cv2
import numpy as np
font = cv2.FONT_HERSHEY_SIMPLEX


def draw_rectangle(img: np.ndarray,
                   bbox: list,
                   bbox_color: tuple = (255, 255, 255),
                   thickness: int = 3,
                   is_opaque: bool = False,
                   alpha: float = 0.5
                   ) -> np.ndarray:
    """Draws the rectangle around the object

    Parameters
    ----------
    img : ndarray
        the actual image
    bbox : list
        a list containing x_min, y_min, x_max and y_max of the rectangle positions
    bbox_color : tuple, optional
        the color of the box, by default (255,255,255)
    thickness : int, optional
        thickness of the outline of the box, by default 3
    is_opaque : bool, optional
        if False, draws a solid rectangular outline. Else, a filled rectangle which is semi transparent, by default False
    alpha : float, optional
        strength of the opacity, by default 0.5

    Returns
    -------
    ndarray
        the image with the bounding box drawn
    """
    output = img.copy()
    if not is_opaque:
        cv2.rectangle(output, (bbox[0], bbox[1]), (bbox[2], bbox[3]),
                      bbox_color, thickness)
    else:
        overlay = img.copy()

        cv2.rectangle(overlay, (bbox[0], bbox[1]), (bbox[2], bbox[3]),
                      bbox_color, -1)
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    return output


def add_label(img,
              label,
              bbox,
              size=1,
              thickness=2,
              draw_bg=True,
              text_bg_color=(255, 255, 255),
              text_color=(0, 0, 0),
              top=True):
    """adds label, inside or outside the rectangle

    Parameters
    ----------
    img : ndarray
        the image on which the label is to be written, preferably the image with the rectangular bounding box drawn
    label : str
        the text (label) to be written
    bbox : list
        a list containing x_min, y_min, x_max and y_max of the rectangle positions
    size : int, optional
        size of the label, by default 1
    thickness : int, optional
        thickness of the label, by default 2
    draw_bg : bool, optional
        if True, draws the background of the text, else just the text is written, by default True
    text_bg_color : tuple, optional
        the background color of the label that is filled, by default (255, 255, 255)
    text_color : tuple, optional
        color of the text (label) to be written, by default (0, 0, 0)
    top : bool, optional
        if True, writes the label on top of the bounding box, else inside, by default True

    Returns
    -------
    ndarray
        the image with the label written
    """

    (label_width, label_height), baseline = cv2.getTextSize(label, font, size, thickness)

    if top:
        label_bg = [bbox[0], bbox[1], bbox[0] + label_width, bbox[1] - label_height - (15 * size)]
        if draw_bg:
            cv2.rectangle(img, (label_bg[0], label_bg[1]),
                          (label_bg[2] + 5, label_bg[3]), text_bg_color, -1)

        cv2.putText(img, label, (bbox[0] + 5, bbox[1] - (15 * size)), font, size, text_color, thickness)
    else:
        label_bg = [bbox[0], bbox[1], bbox[0] + label_width, bbox[1] + label_height + (15 * size)]
        if draw_bg:
            cv2.rectangle(img, (label_bg[0], label_bg[1]),
                          (label_bg[2] + 5, label_bg[3]), text_bg_color, -1)
        cv2.putText(img, label, (bbox[0] + 5, bbox[1] + (16 * size) + (4 * thickness)), font, size, text_color, thickness)
    return img


def add_T_label(img,
                label,
                bbox,
                size=1,
                thickness=2,
                draw_bg=True,
                text_bg_color=(255, 255, 255),
                text_color=(0, 0, 0)):
    """adds a T label to the rectangle, originating from the top of the rectangle

    Parameters
    ----------
    img : ndarray
        the image on which the T label is to be written/drawn, preferably the image with the rectangular bounding box drawn
    label : str
        the text (label) to be written
    bbox : list
        a list containing x_min, y_min, x_max and y_max of the rectangle positions
    size : int, optional
        size of the label, by default 1
    thickness : int, optional
        thickness of the label, by default 2
    draw_bg : bool, optional
        if True, draws the background of the text, else just the text is written, by default True
    text_bg_color : tuple, optional
        the background color of the label that is filled, by default (255, 255, 255)
    text_color : tuple, optional
        color of the text (label) to be written, by default (0, 0, 0)

    Returns
    -------
    ndarray
        the image with the T label drawn/written
    """

    (label_width, label_height), baseline = cv2.getTextSize(label, font, size, thickness)
    # draw vertical line
    x_center = (bbox[0] + bbox[2]) // 2
    y_top = bbox[1] - 50
    cv2.line(img, (x_center, bbox[1]), (x_center, y_top), text_bg_color, 3)

    # draw rectangle with label
    y_bottom = y_top
    y_top = y_bottom - label_height - 5
    x_left = x_center - (label_width // 2) - 5
    x_right = x_center + (label_width // 2) + 5
    if draw_bg:
        cv2.rectangle(img, (x_left, y_top - 30), (x_right, y_bottom),
                      text_bg_color, -1)
    cv2.putText(img, label, (x_left + 5, y_bottom - (8 * size)),
                font, size, text_color, thickness)

    return img


def draw_flag_with_label(img,
                         label,
                         bbox,
                         size=1,
                         thickness=2,
                         write_label=True,
                         line_color=(255, 255, 255),
                         text_bg_color=(255, 255, 255),
                         text_color=(0, 0, 0),
                         ):
    """draws a pole from the middle of the object that is to be labeled and adds the label to the flag

    Parameters
    ----------
    img : ndarray
        the image on which the flag is to be drawn
    label : str
        label that is written inside the flag
    bbox : list
        a list containing x_min, y_min, x_max and y_max of the rectangle positions
    size : int, optional
        size of the label, by default 1
    thickness : int, optional
        thickness of the label, by default 2
    write_label : bool, optional
        if True, writes the label, otherwise, it's just a vertical line, by default True
    line_color : tuple, optional
        the color of the pole of the flag, by default (255, 255, 255)
    text_bg_color : tuple, optional
        the background color of the label that is filled, by default (255, 255, 255)
    text_color : tuple, optional
        color of the text (label) to be written, by default (0, 0, 0)

    Returns
    -------
    ndarray
        the image with flag drawn and the label written in the flag
    """

    # draw vertical line
    (label_width, label_height), baseline = cv2.getTextSize(label, font, size, thickness)

    x_center = (bbox[0] + bbox[2]) // 2
    y_bottom = int((bbox[1] * .75 + bbox[3] * .25))
    y_top = bbox[1] - (y_bottom - bbox[1])

    start_point = (x_center, y_top)
    end_point = (x_center, y_bottom)

    cv2.line(img, start_point, end_point, line_color, 3)

    # write label

    if write_label:
        label_bg = [
            start_point[0], start_point[1], start_point[0] + label_width,
            start_point[1] - label_height - (10 * size)
        ]
        cv2.rectangle(img, (label_bg[0], label_bg[1]),
                      (label_bg[2] + 5, label_bg[3]), text_bg_color, -1)
        cv2.putText(img, label, (start_point[0] + 7, start_point[1] - (13 * size) + 20),
                    font, size, text_color, thickness)
    return img


# THE FOLLOWING ARE OPTIONAL FUNCTIONS THAT CAN BE USED FOR DRAWING OR LABELLING MULTIPLE OBJECTS IN THE SAME
# IMAGE. IN ORDER TO HAVE FULL CONTROL OF YOUR VISUALIZATIONS IT IS ADVISABLE TO USE THE ABOVE FUNCTIONS IN FOR LOOPS
# INSTEAD OF THE FUNCTIONS BELOW


def draw_multiple_rectangles(img,
                             bboxes,
                             bbox_color=(255, 255, 255),
                             thickness=3,
                             is_opaque=False,
                             alpha=0.5):
    """draws multiple rectangles

    img : ndarray
        the actual image
    bboxes : list
        a list of lists, each inner list containing x_min, y_min, x_max and y_max of the rectangle positions
    bbox_color : tuple, optional
        the color of the boxes, by default (255,255,255)
    thickness : int, optional
        thickness of the outline of the boxes, by default 3
    is_opaque : bool, optional
        if False, draws solid rectangular outlines for rectangles. Else, filled rectangles which are semi transparent, by default False
    alpha : float, optional
        strength of the opacity, by default 0.5

    Returns
    -------
    ndarray
        the image with the bounding boxes drawn
    """

    for bbox in bboxes:
        img = draw_rectangle(img, bbox, bbox_color, thickness, is_opaque,
                             alpha)
    return img


def add_multiple_labels(img,
                        labels,
                        bboxes,
                        size=1,
                        thickness=2,
                        draw_bg=True,
                        text_bg_color=(255, 255, 255),
                        text_color=(0, 0, 0),
                        top=True):
    """add labels, inside or outside the rectangles

    Parameters
    ----------
    img : ndarray
        the image on which the labels are to be written, preferably the image with the rectangular bounding boxes drawn
    labels : list
        a list of string of the texts (labels) to be written
    bboxes : list
        a list of lists, each inner list containing x_min, y_min, x_max and y_max of the rectangle positions
    draw_bg : bool, optional
        if True, draws the background of the texts, else just the texts are written, by default True
    text_bg_color : tuple, optional
        the background color of the labels that are filled, by default (255, 255, 255)
    text_color : tuple, optional
        color of the texts (labels) to be written, by default (0, 0, 0)
    top : bool, optional
        if True, writes the labels on top of the bounding boxes, else inside, by default True

    Returns
    -------
    ndarray
        the image with the labels written
    """
    for label, bbox in zip(labels, bboxes):
        img = add_label(img, label, bbox, size, thickness, draw_bg, text_bg_color, text_color,
                        top)

    return img


def add_multiple_T_labels(img,
                          labels,
                          bboxes,
                          draw_bg=True,
                          text_bg_color=(255, 255, 255),
                          text_color=(0, 0, 0)):
    """adds T labels to the rectangles, each originating from the top of the rectangle

    Parameters
    ----------
    img : ndarray
        the image on which the T labels are to be written/drawn, preferably the image with the rectangular bounding boxes drawn
    labels : list
        the texts (labels) to be written
    bboxes : list
        a list of lists, each inner list containing x_min, y_min, x_max and y_max of the rectangle positions
    draw_bg : bool, optional
        if True, draws the background of the texts, else just the texts are written, by default True
    text_bg_color : tuple, optional
        the background color of the labels that are filled, by default (255, 255, 255)
    text_color : tuple, optional
        color of the texts (labels) to be written, by default (0, 0, 0)

    Returns
    -------
    ndarray
        the image with the T labels drawn/written
    """

    for label, bbox in zip(labels, bboxes):
        add_T_label(img, label, bbox, draw_bg, text_bg_color, text_color)

    return img


def draw_multiple_flags_with_labels(img,
                                    labels,
                                    bboxes,
                                    write_label=True,
                                    line_color=(255, 255, 255),
                                    text_bg_color=(255, 255, 255),
                                    text_color=(0, 0, 0)):
    """draws poles from the middle of the objects that are to be labeled and adds the labels to the flags

    Parameters
    ----------
    img : ndarray
        the image on which the flags are to be drawn
    labels : list
        labels that are written inside the flags
    bbox : list
        a list of lists, each inner list containing x_min, y_min, x_max and y_max of the rectangle positions
    write_label : bool, optional
        if True, writes the labels, otherwise, it's just a vertical line for each object, by default True
    line_color : tuple, optional
        the color of the pole of the flags, by default (255, 255, 255)
    text_bg_color : tuple, optional
        the background color of the labels that are filled, by default (255, 255, 255)
    text_color : tuple, optional
        color of the texts (labels) to be written, by default (0, 0, 0)

    Returns
    -------
    ndarray
        the image with flags drawn and the labels written in the flags
    """

    for label, bbox in zip(labels, bboxes):
        img = draw_flag_with_label(img, label, bbox, write_label, line_color,
                                   text_bg_color, text_color)
    return img
