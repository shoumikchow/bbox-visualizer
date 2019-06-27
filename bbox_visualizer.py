import cv2


def draw_rectangle(img, bbox, bbox_color=(255, 255, 255), thickness=3, is_opaque=False, alpha=0.5):
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
        determines if the rectangle should be semi-transparent or not, by default False
    alpha : float, optional
        strenght of the opacity, by default 0.5
    
    Returns
    -------
    ndarray
        the image with the bounding box drawn
    """
    output = img.copy()
    if not is_opaque:
        cv2.rectangle(output, (bbox[0], bbox[1]), (bbox[2], bbox[3]), bbox_color,
                  thickness)
    else:
        overlay = img.copy()
        cv2.rectangle(overlay, (bbox[0], bbox[1]), (bbox[2], bbox[3]), bbox_color,
                  -1)
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    return output

def add_label_to_rectangle(img,
                           label,
                           bbox,
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

    text_width = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

    if top:
        label_bg = [bbox[0], bbox[1], bbox[0] + text_width[0], bbox[1] - 30]
        if draw_bg:
            cv2.rectangle(img, (label_bg[0], label_bg[1]),
                        (label_bg[2] + 5, label_bg[3]), text_bg_color, -1)
        cv2.putText(img, label, (bbox[0] + 5, bbox[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    else:
        label_bg = [bbox[0], bbox[1], bbox[0] + text_width[0], bbox[1] + 30]
        if draw_bg:
            cv2.rectangle(img, (label_bg[0], label_bg[1]),
                        (label_bg[2] + 5, label_bg[3]), text_bg_color, -1)
        cv2.putText(img, label, (bbox[0] + 5, bbox[1] - 5 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    return img


def draw_flag_with_label(img,
                      label,
                      bbox,
                      write_label=True,
                      line_color=(255, 255, 255),
                      text_bg_color=(255, 255, 255),
                      text_color=(0, 0, 0)):
    """draws a pole from the middle of the object that is to be labeled and adds the label to the flag
    
    Parameters
    ----------
    img : ndarray
        the image on which the overlay is to be drawn
    label : str
        label that is written inside the flag
    bbox : list
        a list containing x_min, y_min, x_max and y_max of the rectangle positions
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

    x_center = (bbox[0] + bbox[2]) // 2
    y_bottom = int((bbox[1] * .75 + bbox[3] * .25))
    y_top = bbox[1] - (y_bottom - bbox[1])

    start_point = (x_center, y_top)
    end_point = (x_center, y_bottom)

    cv2.line(img, start_point, end_point, line_color, 3)

    # write label

    if write_label:
        text_width = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        label_bg = [
            start_point[0], start_point[1], start_point[0] + text_width[0],
            start_point[1] + 30
        ]
        cv2.rectangle(img, (label_bg[0], label_bg[1]),
                    (label_bg[2] + 5, label_bg[3]), text_bg_color, -1)
        cv2.putText(img, label, (start_point[0] + 5, start_point[1] - 5 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    return img
