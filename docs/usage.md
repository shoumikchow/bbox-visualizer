# Usage

## Basic Usage

To use bbox-visualizer in a project:

```python
import bbox_visualizer as bbv
import cv2
import numpy as np

# Load an image
image = cv2.imread('image.jpg')

# Draw a bounding box
bbox = (100, 100, 200, 200)  # (x1, y1, x2, y2) format
image = bbv.draw_box(image, bbox)

# Add a label
image = bbv.add_label(image, "Object", bbox)
```

!!! note
    All functions return a new image and never modify the input image, so keep
    the return value (as above) rather than relying on in-place changes.

## Warning Control

The library logs warnings (e.g., when a label falls back to a different style)
through Python's standard `logging` module. To silence them:

```python
import logging

logging.getLogger("bbox_visualizer").setLevel(logging.ERROR)
```

## Drawing Boxes

Basic box drawing:

```python
# Single box
bbox = (100, 100, 200, 200)  # (x1, y1, x2, y2) format
image = bbv.draw_box(image, bbox)

# Multiple boxes
bboxes = [(100, 100, 200, 200), (300, 300, 400, 400)]
image = bbv.draw_multiple_boxes(image, bboxes)

# Multiple boxes with one color per box
image = bbv.draw_multiple_boxes(image, bboxes, bbox_color=[(0, 255, 0), (0, 0, 255)])

# Filled box with transparency
image = bbv.draw_box(image, bbox, is_opaque=True, alpha=0.5)
```

!!! note
    The functions `draw_rectangle` and `draw_multiple_rectangles` are also available
    as aliases for `draw_box` and `draw_multiple_boxes` respectively. Both naming
    conventions work identically.

## Bounding Box Formats

Every drawing function accepts a `bbox_format` keyword argument. The default is
Pascal VOC.

| `bbox_format` | Coordinates | Scale |
|---------------|-------------|-------|
| `"voc"` (default) | `[x_min, y_min, x_max, y_max]` | absolute pixels |
| `"coco"` | `[x_min, y_min, width, height]` | absolute pixels |
| `"yolo"` | `[x_center, y_center, width, height]` | normalized to `[0, 1]` |

```python
# COCO format: [x_min, y_min, width, height]
image = bbv.draw_box(image, [150, 100, 300, 200], bbox_format="coco")

# YOLO format: [x_center, y_center, width, height], normalized to [0, 1].
# Image dimensions are read from the image, so no extra arguments are needed.
image = bbv.draw_box(image, [0.5, 0.4, 0.3, 0.25], bbox_format="yolo")

# Works with the multiple-object variants too
image = bbv.draw_multiple_boxes(image, coco_bboxes, bbox_format="coco")
```

Internally all formats are converted to Pascal VOC before drawing.

## Adding Labels

Simple labels:

```python
# Add label above the box
bbox = (100, 100, 200, 200)
label = "Object"
image = bbv.add_label(image, label, bbox)

# Add label inside the box
image = bbv.add_label(image, label, bbox, top=False)

# Multiple labels
bboxes = [(100, 100, 200, 200), (300, 300, 400, 400)]
labels = ["Object 1", "Object 2"]
image = bbv.add_multiple_labels(image, labels, bboxes)
```

## Special Label Styles

T-shaped and flag labels:

```python
# T-shaped label
image = bbv.add_T_label(image, "Object", bbox)

# Flag-style label
image = bbv.draw_flag_with_label(image, "Object", bbox)

# Multiple T-shaped labels
image = bbv.add_multiple_T_labels(image, labels, bboxes)

# Multiple flag labels
image = bbv.draw_multiple_flags_with_labels(image, labels, bboxes)
```

## Customization

All functions support customization of colors and styles:

```python
# Custom colors
bbox_color = (0, 255, 0)  # Green in BGR
text_color = (0, 0, 0)    # Black
bg_color = (255, 255, 255)  # White

# Draw box with custom color
image = bbv.draw_box(image, bbox, bbox_color=bbox_color)

# Add label with custom colors
image = bbv.add_label(
    image,
    label,
    bbox,
    text_color=text_color,
    text_bg_color=bg_color
)

# T-label with custom style
image = bbv.add_T_label(
    image,
    label,
    bbox,
    text_color=text_color,
    text_bg_color=bg_color
)

# Flag with custom colors
image = bbv.draw_flag_with_label(
    image,
    label,
    bbox,
    line_color=bbox_color,
    text_color=text_color,
    text_bg_color=bg_color
)

# Display the result
cv2.imshow('Image with bounding boxes', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Common Use Cases

### Object Detection Visualization

```python
import bbox_visualizer as bbv
import cv2
import numpy as np

# Simulate object detection results
detections = [
    {"bbox": (50, 50, 150, 150), "label": "Person", "confidence": 0.95},
    {"bbox": (200, 100, 300, 200), "label": "Car", "confidence": 0.87},
    {"bbox": (350, 150, 450, 250), "label": "Dog", "confidence": 0.92}
]

# Load image
image = cv2.imread('detection_image.jpg')

# Visualize each detection
for det in detections:
    bbox = det["bbox"]
    label = f"{det['label']} ({det['confidence']:.2f})"

    # Draw box and label
    image = bbv.draw_box(image, bbox, bbox_color=(0, 255, 0))
    image = bbv.add_label(image, label, bbox)
```

### Multiple Object Classes

```python
# Define color scheme for different classes
class_colors = {
    "person": (0, 255, 0),    # Green
    "car": (255, 0, 0),       # Blue
    "dog": (0, 0, 255),       # Red
    "cat": (255, 255, 0)      # Cyan
}

# Process detections with class-specific colors
for det in detections:
    bbox = det["bbox"]
    label = det["label"]
    color = class_colors.get(label.lower(), (128, 128, 128))

    image = bbv.draw_box(image, bbox, bbox_color=color)
    image = bbv.add_label(image, label, bbox)
```

## Troubleshooting

### Common Issues

**Bounding box format errors**

By default, bounding boxes are expected in Pascal VOC format (x1, y1, x2, y2) where:

- x1, y1: top-left corner coordinates
- x2, y2: bottom-right corner coordinates

If your boxes are in COCO or YOLO format, pass `bbox_format="coco"` or
`bbox_format="yolo"` instead of converting them yourself (see
[Bounding Box Formats](#bounding-box-formats)).

**Color format issues**

OpenCV uses BGR color format, not RGB. For example:

- Red: (0, 0, 255) in BGR
- Green: (0, 255, 0) in BGR
- Blue: (255, 0, 0) in BGR

**Image not displaying**

Ensure you have a display environment or use cv2.imwrite() to save the image:

```python
cv2.imwrite('output.jpg', image)
```

### Performance Tips

- For multiple objects, use the batch functions (e.g., `draw_multiple_boxes`) instead of loops
- Pre-allocate image arrays when possible
- Use appropriate image formats (uint8 for most cases)
- Consider downsampling large images for faster processing

## Getting Help

- Check the `examples/` directory for complete working examples
- Review the API documentation for detailed parameter descriptions
- Open an issue on GitHub for bugs or feature requests
