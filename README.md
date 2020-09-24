# Bbox_Visualizer

This is a simple library which has different functions that lets users draw different types of visualizations. Useful for instances when visualizing objects after object detection.

The bounding box points are expected in the format: `(xmin, ymin, xmax, ymax)`

* Documentation: https://bbox-visualizer.readthedocs.io.
* Free software: MIT license


## Usage:
    
    import bbox_visualizer as bbv


![cover](images/cover.jpg)





#### Photo by [Joshua Earle](https://unsplash.com/@joshuaearle), [Jonas Weckschmied](https://unsplash.com/@jweckschmied) and [Sherzod Max](https://unsplash.com/@sherzodmax) on [Unsplash](https://unsplash.com).  

|                                                 **image**                                                  |                                                    **function**                                                    |
|:----------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------:|
|               ![bbox with label on top](images/bbox_top.jpg "Bouding box with label on top")               |                  bbv.draw_rectangle(img, bbox)<br>add_label(img, label, bbox, top=True)                  |
|             ![bbox with label inside](images/bbox_inside.jpg "Bouding box with label inside")              |                 bbv.draw_rectangle(img, bbox)<br>add_label(img, label, bbox, top=False)                  |
|                  ![bbox with T label](images/bbox_T.jpg "Bouding box with label inside")                   |                      bbv.draw_rectangle(img, bbox)<br>add_T_label(img, label, bbox)                      |
| ![label with flag](images/flag.jpg "Label that looks like a flag, pole originates from inside the object") |                                     bbv.draw_flag_with_label(img, label, bbox)                                     |
|      ![label with opaque overlay](images/overlay.jpg "Opaque bounding box with label inside the box")      | bbv.draw_rectangle(image, bbox, is_opaque=True)<br>add_label(img, label, bbox, draw_bg=False, top=False) |
|      ![multiple bbox](images/bbox_multiple.jpg "Multiple bounding boxes")      | bbv.draw_multiple_rectangles(img, bboxes)<br>bbv.add_multiple_labels(img, labels, bboxes) |
|      ![multiple flags](images/bbox_multiple_flags.jpg "Multiple flags")      | bbv.draw_multiple_flags_with_labels(img, labels, bboxes) |
|      ![multiple T bbox](images/bbox_multiple_T.jpg "Multiple bounding boxes with T labels")      | bbv.draw_multiple_rectangles(img, bboxes)<br>bbv.add_multiple_T_labels(img, labels, bboxes) |

## There are *optional* functions that can draw multiple bounding boxes and/or write multiple labels on the same image, but it is advisable to use the above functions in a loop in order to have full control over your visualizations.

* bbv.draw_multiple_rectangles(img, bboxes)
* bbv.add_multiple_labels(img, labels, bboxes)
* bbv.add_multiple_T_labels(img, labels, bboxes)
* bbv.draw_multiple_flags_with_labels(img, labels, bboxes)

`bboxes` and `labels` are lists in the above examples.


### Credits


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
