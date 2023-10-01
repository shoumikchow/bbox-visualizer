<p align="center">
  <a href="https://bbox-visualizer.readthedocs.io/en/latest/"><img src="./images/bbox_logo.png" alt="bbox"></a>
</p>

<p align="center">This package helps users draw bounding boxes around objects.</p>




[![Documentation Status](https://readthedocs.org/projects/bbox-visualizer/badge/?version=latest)](https://bbox-visualizer.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/bbox-visualizer.svg)](https://pypi.org/project/bbox-visualizer/0.1.0/)
[![Downloads](https://pepy.tech/badge/bbox-visualizer)](https://pepy.tech/project/bbox-visualizer)


* Documentation: [bbox-visualizer](https://bbox-visualizer.readthedocs.io.)
* Free software: MIT license

## Introduction bbox-visuliazer

<p>This package helps users draw bounding boxes around objects, without doing the clumsy math that you'd need to do for positioning the labels. It also has a few different types of visualizations you can use for labeling objects after identifying them.
</p>

**Requeriments:**

- Python 3.8+

**Installation:**

Create env:

```bash
python3 -m venv venv
source env/bin/activate
# Execute pip install to instalation
pip3 install bbox-visualizer
```

Use your env and execute command pip:

```bash
pip install bbox-visualizer
```


**Usage:**

Create script python add import:

```python
import bbox_visualizer as bbv
```

Simple intro use bbox_visualizer:

The bounding box points are expected in the format: `(xmin, ymin, xmax, ymax)`

```python
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

img_with_boxes = bbv.add_multiple_labels(img_with_boxes, labels, bboxes)
```

**Result:**

<p>
  <a href="https://bbox-visualizer.readthedocs.io/en/latest/"><img src="images/cover.jpg" alt="bbox" height='300px' width='500px'></a>
</p>

### Notebooks examples

You can also test the tool using one of our notebooks.

- [Single Label](https://github.com/shoumikchow/bbox-visualizer/blob/dev/examples/single_object_example.ipynb)
- [Multi Label](https://github.com/shoumikchow/bbox-visualizer/blob/dev/examples/multiple_objects_example.ipynb)

## Function labels 

<table>
  <tr>
    <th>Image</th>
    <th>Function</th>
  </tr>
  <tr>
    <td>
        <p align="center">
            <a href="https://bbox-visualizer.readthedocs.io/en/latest/"><img src="images/bbox_top.jpg" alt="bbox" height='200px' width='400px'></a>
        </p>
    </td>
    <td>img = bbv.draw_rectangle(img, bbox)<br>img = bbv.add_label(img, label, bbox, top=True)
    </td>
  </tr>
  <tr>
    <td>
        <p align="center">
            <a href="https://bbox-visualizer.readthedocs.io/en/latest/"><img src="images/bbox_T.jpg" alt="bbox" height='200px' width='400px'></a>
        </p>
    </td>
    <td>img = bbv.draw_rectangle(img, bbox)<br>img = bbv.add_T_label(img, label, bbox)</td>
  </tr>
  <tr>
    <td>
        <p align="center">
            <a href="https://bbox-visualizer.readthedocs.io/en/latest/"><img src="images/flag.jpg" alt="bbox" height='200px' width='400px'></a>
        </p>
    </td>
    <td>img = bbv.draw_flag_with_label(img, label, bbox)</td>
  </tr>
  <tr>
    <td>
        <p align="center">
            <a href="https://bbox-visualizer.readthedocs.io/en/latest/"><img src="images/bbox_inside.jpg" alt="bbox" height='200px' width='400px'></a>
        </p>
    </td>
    <td>img = bbv.draw_rectangle(img, bbox)<br>img = bbv.add_label(img, label, bbox, top=False)</td>
  </tr>
  <tr>
    <td>
        <p align="center">
            <a href="https://bbox-visualizer.readthedocs.io/en/latest/"><img src="images/overlay.jpg" alt="bbox" height='200px' width='400px'></a>
        </p>
    </td>
    <td>img = bbv.draw_rectangle(image, bbox, is_opaque=True)<br>img = bbv.add_label(img, label, bbox, draw_bg=False, top=False)</td>
  </tr>
</table>


There are *optional* functions that can draw multiple bounding boxes and/or write multiple labels on the same image, but it is advisable to use the above functions in a loop in order to have full control over your visualizations.

* bbv.draw_multiple_rectangles(img, bboxes)
* bbv.add_multiple_labels(img, labels, bboxes)
* bbv.add_multiple_T_labels(img, labels, bboxes)
* bbv.draw_multiple_flags_with_labels(img, labels, bboxes)

`bboxes` and `labels` are lists in the above examples.


## Credits

Photos by

- [Joshua Earle](https://unsplash.com/@joshuaearle) 
- [Jonas Weckschmied](https://unsplash.com/@jweckschmied)
- [Sherzod Max](https://unsplash.com/@sherzodmax)
- [Unsplash](https://unsplash.com)

This package was created with Cookiecutter and the `audreyr/cookiecutter-pypackage` project template.
