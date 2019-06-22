# Annotation-Visualizer

This is a simple script which has different functions that lets users draw different types of visualizations. Useful for instances when visualizing objects after object detection.

#### Photo by Joshua Earle on Unsplash

|                                                     **image**                                                      |                         **function**                          |
| :----------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------: |
|               ![bbox with label on top](images/bbox_top.jpg "Bouding box with label on top")               | draw_rectangle(...)<br>add_label_to_rectangle(..., top=True)  |
|             ![bbox with label inside](images/bbox_inside.jpg "Bouding box with label inside")              | draw_rectangle(...)<br>add_label_to_rectangle(..., top=False) |
| ![label with flag](images/flag.jpg "Label that looks like a flag, pole originates from inside the object") |                   draw_flag_with_label(...)                   |
|      ![label with opaque overlay](images/overlay.jpg "Opaque bounding box with label inside the box")      |               draw_rectangle_overlay(..., alpha=0.5)               |
