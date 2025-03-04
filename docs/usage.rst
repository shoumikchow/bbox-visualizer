Usage
=====

To use bbox-visualizer in a project:

.. code-block:: python

    import bbox_visualizer as bbv
    import cv2
    import numpy as np

    # Load an image
    image = cv2.imread('image.jpg')

    # Example bounding box in (xmin, ymin, xmax, ymax) format
    bbox = (100, 100, 200, 200)
    label = "Object"

    # Draw bounding box with label
    image_with_box = bbv.draw_rectangle(image, bbox)
    image_with_label = bbv.add_label(image_with_box, label, bbox)

    # Or use multiple bounding boxes
    bboxes = [(100, 100, 200, 200), (300, 300, 400, 400)]
    labels = ["Object 1", "Object 2"]

    # Draw multiple boxes with labels
    for bbox, label in zip(bboxes, labels):
        image = bbv.draw_rectangle(image, bbox)
        image = bbv.add_label(image, label, bbox)

    # Display the result
    cv2.imshow('Image with bounding boxes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 