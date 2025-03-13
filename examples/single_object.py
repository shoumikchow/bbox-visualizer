import json

import cv2

import bbox_visualizer as bbv

img = cv2.imread("../images/source_single.jpg")
annotation = json.load(open("../images/source_single.json"))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

points = annotation["shapes"][0]["points"]
label = annotation["shapes"][0]["label"]
(xmin, ymin), (xmax, ymax) = points
bbox = [xmin, ymin, xmax, ymax]

img_with_box = bbv.draw_rectangle(img, bbox)
img_with_box_2 = img_with_box.copy()

img_label = bbv.add_label(img_with_box, label, bbox)
img_T_label = bbv.add_T_label(img_with_box_2, label, bbox)

img_flag = bbv.draw_flag_with_label(img, label, bbox)
