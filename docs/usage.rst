Usage
=====

Basic Usage
----------

To use bbox-visualizer in a project:

.. code-block:: python

    import bbox_visualizer as bbv
    import cv2
    import numpy as np

    # Load an image
    image = cv2.imread('image.jpg')

Warning Control
-------------

The library provides functionality to control warning messages:

.. code-block:: python

    # Suppress all warnings
    bbv.suppress_warnings(True)

    # Enable warnings
    bbv.suppress_warnings(False)

    # Temporarily suppress warnings using context manager
    with bbv.warnings_suppressed():
        # Warnings will be suppressed in this block
        image = bbv.draw_flag_with_label(image, "Object", bbox)

Drawing Rectangles
----------------

Basic rectangle drawing:

.. code-block:: python

    # Single rectangle
    bbox = (100, 100, 200, 200)  # (x1, y1, x2, y2) format
    image = bbv.draw_rectangle(image, bbox)

    # Multiple rectangles
    bboxes = [(100, 100, 200, 200), (300, 300, 400, 400)]
    image = bbv.draw_multiple_rectangles(image, bboxes)

    # Filled rectangle with transparency
    image = bbv.draw_rectangle(image, bbox, is_opaque=True, alpha=0.5)

Adding Labels
-----------

Simple labels:

.. code-block:: python

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

Special Label Styles
-----------------

T-shaped and flag labels:

.. code-block:: python

    # T-shaped label
    image = bbv.add_T_label(image, "Object", bbox)

    # Flag-style label
    image = bbv.draw_flag_with_label(image, "Object", bbox)

    # Multiple T-shaped labels
    image = bbv.add_multiple_T_labels(image, labels, bboxes)

    # Multiple flag labels
    image = bbv.draw_multiple_flags_with_labels(image, labels, bboxes)

Customization
-----------

All functions support customization of colors and styles:

.. code-block:: python

    # Custom colors
    bbox_color = (0, 255, 0)  # Green in BGR
    text_color = (0, 0, 0)    # Black
    bg_color = (255, 255, 255)  # White

    # Draw rectangle with custom color
    image = bbv.draw_rectangle(image, bbox, bbox_color=bbox_color)

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

Common Use Cases
--------------

Object Detection Visualization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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
        
        # Draw rectangle and label
        image = bbv.draw_rectangle(image, bbox, bbox_color=(0, 255, 0))
        image = bbv.add_label(image, label, bbox)

Multiple Object Classes
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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
        
        image = bbv.draw_rectangle(image, bbox, bbox_color=color)
        image = bbv.add_label(image, label, bbox)

Troubleshooting
-------------

Common Issues
~~~~~~~~~~~~

**Bounding box format errors**
    Make sure your bounding boxes are in (x1, y1, x2, y2) format where:
    - x1, y1: top-left corner coordinates
    - x2, y2: bottom-right corner coordinates

**Color format issues**
    OpenCV uses BGR color format, not RGB. For example:
    - Red: (0, 0, 255) in BGR
    - Green: (0, 255, 0) in BGR
    - Blue: (255, 0, 0) in BGR

**Image not displaying**
    Ensure you have a display environment or use cv2.imwrite() to save the image:
    
    .. code-block:: python
    
        cv2.imwrite('output.jpg', image)

Performance Tips
~~~~~~~~~~~~~~

- For multiple objects, use the batch functions (e.g., `draw_multiple_rectangles`) instead of loops
- Pre-allocate image arrays when possible
- Use appropriate image formats (uint8 for most cases)
- Consider downsampling large images for faster processing

Getting Help
-----------

- Check the `examples/` directory for complete working examples
- Review the API documentation for detailed parameter descriptions
- Open an issue on GitHub for bugs or feature requests 