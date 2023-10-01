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


IMG = cv2.imread('/bbox_visualizer/tests/assets/source_single.jpg')
ANNOTATION = json.load(open('/bbox_visualizer/tests/assets/source_single.json'))
IMG = cv2.cvtColor(IMG, cv2.COLOR_BGR2RGB)


def test_draw_rectangle():
    points = ANNOTATION['shapes'][0]['points']
    (xmin, ymin), (xmax, ymax) = points
    bbox = [xmin, ymin, xmax, ymax]
    img_with_box = bbv.draw_rectangle(IMG, bbox)
    assert isinstance(img_with_box, np.ndarray)


def test_add_label():
    points = ANNOTATION['shapes'][0]['points']
    label = ANNOTATION['shapes'][0]['label']
    (xmin, ymin), (xmax, ymax) = points
    bbox = [xmin, ymin, xmax, ymax]
    img_with_box = bbv.draw_rectangle(IMG, bbox)

    assert isinstance(img_with_box, np.ndarray)

    img_label = bbv.add_label(img_with_box, label, bbox)

    assert isinstance(img_label, np.ndarray)


def test_add_T_label():
    points = ANNOTATION['shapes'][0]['points']
    label = ANNOTATION['shapes'][0]['label']
    (xmin, ymin), (xmax, ymax) = points
    bbox = [xmin, ymin, xmax, ymax]
    img_with_box = bbv.draw_rectangle(IMG, bbox)

    assert isinstance(img_with_box, np.ndarray)

    img_label = bbv.add_T_label(img_with_box, label, bbox)

    assert isinstance(img_label, np.ndarray)


def test_add_flag_label():
    points = ANNOTATION['shapes'][0]['points']
    label = ANNOTATION['shapes'][0]['label']
    (xmin, ymin), (xmax, ymax) = points
    bbox = [xmin, ymin, xmax, ymax]

    img_flag_label = bbv.draw_flag_with_label(IMG, label, bbox)

    assert isinstance(img_flag_label, np.ndarray)