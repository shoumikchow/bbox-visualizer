import logging

import numpy as np
import pytest

from bbox_visualizer.core import flags, labels, rectangle
from bbox_visualizer.core._utils import suppress_warnings, warnings_suppressed


@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    return np.zeros((100, 100, 3), dtype=np.uint8)


@pytest.fixture
def sample_bbox():
    """Create a sample bounding box for testing."""
    return [10, 10, 50, 50]  # x_min, y_min, x_max, y_max


@pytest.fixture
def sample_label():
    """Create a sample label for testing."""
    return "test"


def test_check_and_modify_bbox(sample_image):
    """Test bbox validation and modification."""
    # Test negative coordinates
    bbox = [-10, -10, 50, 50]
    result = rectangle._check_and_modify_bbox(bbox, sample_image.shape)
    assert result[0] >= 0 and result[1] >= 0

    # Test coordinates exceeding image size
    bbox = [10, 10, 200, 200]
    result = rectangle._check_and_modify_bbox(bbox, sample_image.shape)
    assert result[2] <= sample_image.shape[1]
    assert result[3] <= sample_image.shape[0]

    # Test with margin
    bbox = [-10, -10, 200, 200]
    margin = 5
    result = rectangle._check_and_modify_bbox(bbox, sample_image.shape, margin)
    assert result[0] == margin
    assert result[1] == margin
    assert result[2] == sample_image.shape[1] - margin
    assert result[3] == sample_image.shape[0] - margin


def test_draw_rectangle_basic(sample_image, sample_bbox):
    """Test basic rectangle drawing functionality."""
    result = rectangle.draw_rectangle(sample_image, sample_bbox)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    # Check if rectangle was drawn (should have some non-zero pixels)
    assert np.sum(result) > 0


def test_draw_rectangle_opaque(sample_image, sample_bbox):
    """Test opaque rectangle drawing."""
    result = rectangle.draw_rectangle(
        sample_image, sample_bbox, is_opaque=True, alpha=0.5
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0


def test_add_label(sample_image, sample_bbox, sample_label, caplog):
    """Test adding label to bounding box."""
    # Test normal case with top=True and enough space
    bbox_with_space = [10, 30, 50, 70]  # Plenty of space above and below
    result = labels.add_label(sample_image, sample_label, bbox_with_space, top=True)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

    # Test normal case with top=False and enough space
    result = labels.add_label(sample_image, sample_label, bbox_with_space, top=False)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

    # Test with draw_bg=False for both top and bottom positions
    result = labels.add_label(
        sample_image, sample_label, bbox_with_space, draw_bg=False, top=True
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

    result = labels.add_label(
        sample_image, sample_label, bbox_with_space, draw_bg=False, top=False
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

    # Test label at top when there's not enough space
    bbox_at_top = [10, 5, 50, 20]  # Very close to top of image
    result = labels.add_label(sample_image, sample_label, bbox_at_top, top=True)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape

    # Test label at bottom when there's not enough space
    bbox_at_bottom = [10, 80, 50, 99]  # Very close to bottom of image
    result = labels.add_label(sample_image, sample_label, bbox_at_bottom, top=False)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape


def test_add_T_label(sample_image, sample_bbox, sample_label, caplog):
    """Test adding T-label to bounding box."""
    # Test normal case with enough space and background
    bbox_with_space = [40, 80, 60, 95]  # Plenty of space above (at least 50 pixels)
    result = flags.add_T_label(
        sample_image,
        sample_label,
        bbox_with_space,
        draw_bg=True,
        text_bg_color=(255, 0, 0),  # Red background to ensure visibility
        size=1,
        thickness=2,  # Explicit size and thickness
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

    # Test with draw_bg=False
    result = flags.add_T_label(
        sample_image,
        sample_label,
        bbox_with_space,
        draw_bg=False,
        text_color=(0, 255, 0),  # Green text to ensure visibility
        size=1,
        thickness=2,  # Explicit size and thickness
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

    # Test with custom size and thickness
    result = flags.add_T_label(
        sample_image,
        sample_label,
        bbox_with_space,
        size=2,
        thickness=3,
        text_bg_color=(0, 0, 255),  # Blue background
        draw_bg=True,  # Explicit background drawing
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

    # Test with a long label to ensure text width calculation
    long_label = "This is a very long label"
    result = flags.add_T_label(
        sample_image,
        long_label,
        bbox_with_space,
        draw_bg=True,
        text_bg_color=(255, 255, 0),  # Yellow background
        size=1,
        thickness=2,  # Explicit size and thickness
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

    # Test with a bbox that has enough vertical space but is close to image edges
    bbox_near_edge = [5, 80, 25, 95]  # Close to left edge but plenty of space above
    result = flags.add_T_label(
        sample_image,
        sample_label,
        bbox_near_edge,
        draw_bg=True,
        text_bg_color=(255, 0, 255),  # Magenta background
        size=1,
        thickness=2,  # Explicit size and thickness
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

    # Test fallback when label would go out of frame at top
    bbox_at_top = [10, 5, 50, 20]  # Very close to top of image
    caplog.clear()
    with caplog.at_level(logging.WARNING):
        result = flags.add_T_label(
            sample_image,
            sample_label,
            bbox_at_top,
            draw_bg=True,
            text_bg_color=(128, 128, 128),  # Gray background
        )
    assert (
        "Labelling style 'T' going out of frame. Falling back to normal labeling."
        in caplog.text
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape

    # Test fallback when label would go out of frame on the right side
    bbox_at_right = [80, 30, 99, 50]  # Very close to right edge of image
    caplog.clear()
    with caplog.at_level(logging.WARNING):
        result = flags.add_T_label(
            sample_image,
            sample_label,
            bbox_at_right,
            draw_bg=True,
            text_bg_color=(128, 128, 128),  # Gray background
        )
    assert (
        "Labelling style 'T' going out of frame. Falling back to normal labeling."
        in caplog.text
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape


def test_draw_flag_with_label(sample_image, sample_bbox, sample_label, caplog):
    """Test drawing flag with label."""
    # Test normal case
    result = flags.draw_flag_with_label(sample_image, sample_label, sample_bbox)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

    # Test fallback when flag would go out of frame
    bbox_at_top = [10, 0, 50, 10]  # At the very top of image
    caplog.clear()  # Clear any previous log messages
    with caplog.at_level(logging.WARNING):
        result = flags.draw_flag_with_label(sample_image, sample_label, bbox_at_top)
    assert (
        "Labelling style 'Flag' going out of frame. Falling back to normal labeling."
        in caplog.text
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape


def test_draw_multiple_rectangles(sample_image):
    """Test drawing multiple rectangles."""
    bboxes = [[10, 10, 30, 30], [50, 50, 70, 70]]
    result = rectangle.draw_multiple_rectangles(sample_image, bboxes)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0


def test_add_multiple_labels(sample_image):
    """Test adding multiple labels."""
    bboxes = [[10, 10, 30, 30], [50, 50, 70, 70]]
    labels_list = ["obj1", "obj2"]
    result = labels.add_multiple_labels(sample_image, labels_list, bboxes)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0


def test_add_multiple_T_labels(sample_image):
    """Test adding multiple T-labels."""
    bboxes = [[10, 10, 30, 30], [50, 50, 70, 70]]
    labels_list = ["obj1", "obj2"]
    result = flags.add_multiple_T_labels(sample_image, labels_list, bboxes)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0


def test_draw_multiple_flags_with_labels(sample_image):
    """Test drawing multiple flags with labels."""
    bboxes = [[10, 10, 30, 30], [50, 50, 70, 70]]
    labels_list = ["obj1", "obj2"]
    result = flags.draw_multiple_flags_with_labels(sample_image, labels_list, bboxes)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0


def test_invalid_bbox_values(sample_image):
    """Test handling of invalid bbox values."""
    # Test with empty bbox
    with pytest.raises(ValueError):
        rectangle.draw_rectangle(sample_image, [])

    # Test with invalid bbox format
    with pytest.raises(ValueError):
        rectangle.draw_rectangle(sample_image, [1, 2, 3])  # Missing one coordinate

    # Test with invalid coordinate order (x_min > x_max or y_min > y_max)
    with pytest.raises(ValueError):
        rectangle.draw_rectangle(sample_image, [50, 10, 10, 50])  # x_min > x_max
    with pytest.raises(ValueError):
        rectangle.draw_rectangle(sample_image, [10, 50, 50, 10])  # y_min > y_max


def test_empty_inputs():
    """Test handling of empty inputs for multiple object functions."""
    img = np.zeros((100, 100, 3), dtype=np.uint8)

    # Test with empty lists
    with pytest.raises(ValueError):
        rectangle.draw_multiple_rectangles(img, [])
    with pytest.raises(ValueError):
        labels.add_multiple_labels(img, [], [])
    with pytest.raises(ValueError):
        flags.add_multiple_T_labels(img, [], [])
    with pytest.raises(ValueError):
        flags.draw_multiple_flags_with_labels(img, [], [])


def test_color_parameters(sample_image, sample_bbox):
    """Test color parameter handling."""
    # Test invalid color values
    with pytest.raises(ValueError):
        rectangle.draw_rectangle(
            sample_image, sample_bbox, bbox_color=(300, 0, 0)
        )  # Invalid RGB
    with pytest.raises(ValueError):
        labels.add_label(
            sample_image, "test", sample_bbox, text_color=(-1, 0, 0)
        )  # Invalid RGB
    with pytest.raises(ValueError):
        flags.add_T_label(
            sample_image, "test", sample_bbox, text_bg_color=(0, 0, 300)
        )  # Invalid RGB


def test_warning_suppression(sample_image, sample_bbox, sample_label, caplog):
    """Test warning suppression functionality."""
    # Test global warning suppression
    suppress_warnings(True)
    with caplog.at_level(logging.WARNING):
        flags.draw_flag_with_label(sample_image, sample_label, [10, 0, 50, 10])
    assert len(caplog.records) == 0  # No warnings should be logged

    # Test warning re-enabling
    suppress_warnings(False)
    with caplog.at_level(logging.WARNING):
        flags.draw_flag_with_label(sample_image, sample_label, [10, 0, 50, 10])
    assert len(caplog.records) > 0  # Warnings should be logged
    assert "Labelling style 'Flag' going out of frame" in caplog.text

    # Test context manager
    caplog.clear()
    with warnings_suppressed():
        with caplog.at_level(logging.WARNING):
            flags.draw_flag_with_label(sample_image, sample_label, [10, 0, 50, 10])
    assert len(caplog.records) == 0  # No warnings should be logged

    # Test warning restoration after context manager
    with caplog.at_level(logging.WARNING):
        flags.draw_flag_with_label(sample_image, sample_label, [10, 0, 50, 10])
    assert len(caplog.records) > 0  # Warnings should be logged again
    assert "Labelling style 'Flag' going out of frame" in caplog.text
