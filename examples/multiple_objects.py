import json

import bbox_visualizer as bbv
import cv2

img = cv2.imread('../images/source_multiple.jpg')
annotation = json.load(open('../images/source_multiple.json'))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

labels = []
bboxes = []
for shape in annotation['shapes']:
    labels.append(shape['label'])
    mins = shape['points'][0]
    maxs = shape['points'][1]
    bboxes.append(mins + maxs)

img_with_boxes = bbv.draw_multiple_rectangles(img, bboxes)
img_with_boxes_2 = img_with_boxes.copy()

img_with_boxes = bbv.add_multiple_labels(img_with_boxes, labels, bboxes)
img_with_T_labels = bbv.add_multiple_T_labels(img_with_boxes_2, labels, bboxes)

img_with_flags = bbv.draw_multiple_flags_with_labels(img, labels, bboxes)
