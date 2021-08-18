import json

import bbox_visualizer as bbv
import cv2

img = cv2.imread('test_images/source_bird.jpg')
annotation = json.load(open('test_images/source_bird.json'))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

points = annotation['shapes'][0]['points']
label = annotation['shapes'][0]['label']
(xmin, ymin), (xmax, ymax) = points
bbox = [xmin, ymin, xmax, ymax]

img_with_box = bbv.draw_rectangle(img, bbox)
img_with_box_2 = img_with_box.copy()

img_label = bbv.add_label(img_with_box, label, bbox)
img_T_label = bbv.add_T_label(img_with_box_2, label, bbox)

img_flag = bbv.draw_flag_with_label(img, label, bbox)

cv2.imshow("img_with_box", img_with_box)
cv2.imshow("img_with_T_label", img_T_label)
cv2.imshow("img_with_flag", img_flag)

cv2.waitKey(0)
cv2.destroyAllWindows()
