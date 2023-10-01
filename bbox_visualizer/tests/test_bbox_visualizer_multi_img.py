import json
import cv2
import os

import numpy as np 
import bbox_visualizer as bbv

def test_dir_files():
    path_assets = os.path.join(
        '/bbox_visualizer',
        'tests/assets',
        )
    assert os.path.exists(path_assets)


IMG = cv2.imread('/bbox_visualizer/tests/assets/source_multiple.jpg')
ANNOTATION = json.load(open('/bbox_visualizer/tests/assets/source_multiple.json'))
IMG = cv2.cvtColor(IMG, cv2.COLOR_BGR2RGB)


def test_multiple_draw_rectangles():
    labels = []
    bboxes = []
    for shape in ANNOTATION['shapes']:
        labels.append(shape['label'])
        mins = shape['points'][0]
        maxs = shape['points'][1]
        bboxes.append(mins + maxs)
    img_with_box = bbv.draw_multiple_rectangles(IMG, bboxes)
    assert isinstance(img_with_box, np.ndarray)


def test_add_multiple_labels():
    labels = []
    bboxes = []
    for shape in ANNOTATION['shapes']:
        labels.append(shape['label'])
        mins = shape['points'][0]
        maxs = shape['points'][1]
        bboxes.append(mins + maxs)
    img_with_boxes = bbv.draw_multiple_rectangles(IMG, bboxes)
    assert isinstance(img_with_boxes, np.ndarray)

    img_with_boxes = bbv.add_multiple_labels(img_with_boxes, labels, bboxes)
    assert isinstance(img_with_boxes, np.ndarray)


"""def test_add_multiple_T_labels():
    labels = []
    bboxes = []
    for shape in ANNOTATION['shapes']:
        labels.append(shape['label'])
        mins = shape['points'][0]
        maxs = shape['points'][1]
        bboxes.append(mins + maxs)
    img_with_boxes = bbv.draw_multiple_rectangles(IMG, bboxes)
    assert isinstance(img_with_boxes, np.ndarray)

    img_with_boxes = bbv.add_multiple_T_labels(img_with_boxes, labels, bboxes)
    assert isinstance(img_with_boxes, np.ndarray)"""


def test_draw_multiple_flags_with_labels():
    labels = []
    bboxes = []
    for shape in ANNOTATION['shapes']:
        labels.append(shape['label'])
        mins = shape['points'][0]
        maxs = shape['points'][1]
        bboxes.append(mins + maxs)

    img_with_flags = bbv.draw_multiple_flags_with_labels(IMG, labels, bboxes)
    assert isinstance(img_with_flags, np.ndarray)