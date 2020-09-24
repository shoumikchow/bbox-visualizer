import json

import bbox_visualizer as bbv
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('../images/source_multiple.jpg')
annotation = json.load(open('../images/source_multiple.json'))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

labels = []
bboxes = []
for shape in annotation['shapes']:
    labels.append(shape['label'])
    mins = shape['points'][0]
    maxs = shape['points'][1]
    # xmin, ymin, xmax, ymax = shape['points']
    bboxes.append(mins + maxs)

img_with_boxes = bbv.draw_multiple_rectangles(img, bboxes)
img_with_boxes = bbv.add_multiple_labels(img, labels, bboxes)
plt.imshow(img_with_boxes)
plt.show()
