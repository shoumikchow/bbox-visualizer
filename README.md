# Bbox-Visualizer

This is a simple script which has different functions that lets users draw different types of visualizations. Useful for instances when visualizing objects after object detection.

* Free software: MIT license
* Documentation: https://bbox-visualizer.readthedocs.io.

#### Photo by Joshua Earle on Unsplash

|                                                 **image**                                                  |                                         **function**                                         |
| :--------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------: |
|               ![bbox with label on top](images/bbox_top.jpg "Bouding box with label on top")               |                 draw_rectangle(img, bbox, ...)<br>add_label(img, label, bbox, top=True, ...)                 |c
|             ![bbox with label inside](images/bbox_inside.jpg "Bouding box with label inside")              |                draw_rectangle(img, bbox, ...)<br>add_label(img, label, bbox, top=False, ...)                 |
|                  ![bbox with T label](images/bbox_T.jpg "Bouding box with label inside")                   |                     draw_rectangle(img, bbox, ...)<br>add_T_label(img, label, bbox, ...)                     |
| ![label with flag](images/flag.jpg "Label that looks like a flag, pole originates from inside the object") |                                  draw_flag(img, label, bbox)                                   |
|      ![label with opaque overlay](images/overlay.jpg "Opaque bounding box with label inside the box")      | draw_rectangle(image, bbox, is_opaque=True, ...)<br>add_label(img, label, bbox, draw_bg=False, top=False, ...) |


## There are *optional* functions that can draw multiple bounding boxes and/or write multiple labels on the same image, but it is advisable to use the above functions in a loop in order to have full control over your visualizations. Nonetheless, the optional functions are as follows:

* draw_rectangles(..., bboxes, ...)
* add_multiple_labels(..., labels, bboxes, ...)
* add_multiple_T_labels(..., labels, bboxes, ...)
* draw_multiple_flags(..., labels, bboxes, ...)

`bboxes` and `labels` are lists in the above examples.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
