# Annotation-Visualizer

This is a simple script which has different functions that lets users draw different types of visualizations. Useful for instances when visualizing objects after object detection.

#### Photo by Joshua Earle on Unsplash

|                                                 **image**                                                  |                                         **function**                                         |
| :--------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------: |
|               ![bbox with label on top](images/bbox_top.jpg "Bouding box with label on top")               |                 draw_rectangle(...)<br>add_label_to_rectangle(..., top=True)                 |
|             ![bbox with label inside](images/bbox_inside.jpg "Bouding box with label inside")              |                draw_rectangle(...)<br>add_label_to_rectangle(..., top=False)                 |
|                  ![bbox with T label](images/bbox_T.jpg "Bouding box with label inside")                   |                     draw_rectangle(...)<br>add_T_label_to_rectangle(...)                     |
| ![label with flag](images/flag.jpg "Label that looks like a flag, pole originates from inside the object") |                                  draw_flag_with_label(...)                                   |
|      ![label with opaque overlay](images/overlay.jpg "Opaque bounding box with label inside the box")      | draw_rectangle(..., is_opaque=True)<br>add_label_to_rectangle(..., draw_bg=False, top=False) |


## There are *optional* functions that can draw multiple bounding boxes and/or write multiple labels on the same image, but it is advisable to use the above functions in a loop in order to have full control over your visualizations. Nonetheless, the optional functions are as follows:

* draw_rectangles(..., bboxes, ...)
* add_labels_to_rectangles(..., labels, bboxes, ...)
* add_T_labels_to_rectangles(..., labels, bboxes, ...)
* draw_flags_with_labels(..., labels, bboxes, ...)

`bboxes` and `labels` are lists in the above examples.