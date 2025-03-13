"""
Example script demonstrating bbox-visualizer usage with a single object.
This script shows how to:
1. Load an image and its annotation
2. Draw a bounding box
3. Add different types of labels (normal, T-label, and flag)
"""

import json

import cv2

import bbox_visualizer as bbv


def main():
    # Load image and annotation
    img = cv2.imread("../images/test_images/source_bird.jpg")
    if img is None:
        print("Error: Could not load image. Please check the path.")
        return

    try:
        annotation = json.load(open("../images/test_images/source_bird.json"))
    except FileNotFoundError:
        print("Error: Could not load annotation file. Please check the path.")
        return

    # Convert to RGB for better visualization
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Extract bounding box and label from annotation
    points = annotation["shapes"][0]["points"]
    label = annotation["shapes"][0]["label"]
    (xmin, ymin), (xmax, ymax) = points
    bbox = [xmin, ymin, xmax, ymax]

    # Draw different visualizations
    img_with_box = bbv.draw_rectangle(img, bbox)
    img_with_box_2 = img_with_box.copy()

    img_T_label = bbv.add_T_label(img_with_box_2, label, bbox)
    img_flag = bbv.draw_flag_with_label(img, label, bbox)

    # Display results
    cv2.imshow("Bounding Box", img_with_box)
    cv2.imshow("With T-label", img_T_label)
    cv2.imshow("With Flag", img_flag)

    print("Press any key to close the windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
