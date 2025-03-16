"""
Example script demonstrating bbox-visualizer usage with multiple objects.
This script shows how to:
1. Load an image and its annotations
2. Draw multiple bounding boxes
3. Add different types of labels (normal, T-label, and flags) for multiple objects
"""

import json

import cv2

import bbox_visualizer as bbv


def main():
    # Load image and annotation
    img = cv2.imread("../images/test_images/source_multiple_cats.jpg")
    if img is None:
        print("Error: Could not load image. Please check the path.")
        return

    try:
        annotation = json.load(open("../images/test_images/source_multiple_cats.json"))
    except FileNotFoundError:
        print("Error: Could not load annotation file. Please check the path.")
        return

    # Extract labels and bounding boxes from annotation
    labels = []
    bboxes = []
    for shape in annotation["shapes"]:
        labels.append(shape["label"])
        mins = shape["points"][0]  # [xmin, ymin]
        maxs = shape["points"][1]  # [xmax, ymax]
        bboxes.append(mins + maxs)  # [xmin, ymin, xmax, ymax]

    # Draw different visualizations
    img_with_boxes = bbv.draw_multiple_rectangles(img, bboxes)
    img_with_boxes_2 = img_with_boxes.copy()

    # Add different types of labels
    img_with_labels = bbv.add_multiple_labels(img_with_boxes, labels, bboxes)
    img_with_T_labels = bbv.add_multiple_T_labels(img_with_boxes_2, labels, bboxes)
    img_with_flags = bbv.draw_multiple_flags_with_labels(img, labels, bboxes)

    # Display results
    cv2.imshow("Boxes with Labels", img_with_labels)
    cv2.imshow("Boxes with T-labels", img_with_T_labels)
    cv2.imshow("Boxes with Flags", img_with_flags)

    print("Press any key to close the windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
