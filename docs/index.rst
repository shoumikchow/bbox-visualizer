Welcome to bbox-visualizer's documentation!
=====================================

bbox-visualizer is a Python package that provides different ways to visualize objects given bounding box data.
The package is organized into several modules for different visualization needs:

* **Rectangle Drawing**: Basic functions for drawing bounding boxes
* **Label Drawing**: Functions for adding text labels to boxes
* **Special Labels**: T-shaped and flag-style label visualizations

Quick Start
----------

Get started with bbox-visualizer in just a few lines:

.. code-block:: python

    import bbox_visualizer as bbv
    import cv2
    import numpy as np

    # Create a sample image
    image = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Draw a bounding box with label
    bbox = (100, 100, 300, 200)
    image = bbv.draw_rectangle(image, bbox, bbox_color=(0, 255, 0))
    image = bbv.add_label(image, "Object", bbox)
    
    # Display the result
    cv2.imshow('Result', image)
    cv2.waitKey(0)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api

Examples
--------

Check out the Jupyter notebook examples in the `examples/` directory:
* `single_object_example.ipynb` - Basic usage with single objects
* `multiple_objects_example.ipynb` - Working with multiple bounding boxes

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
