import pytest
import numpy as np
import cv2
from bbox_visualizer import bbox_visualizer

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

def test_draw_rectangle_basic(sample_image, sample_bbox):
    """Test basic rectangle drawing functionality."""
    result = bbox_visualizer.draw_rectangle(sample_image, sample_bbox)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    # Check if rectangle was drawn (should have some non-zero pixels)
    assert np.sum(result) > 0

def test_draw_rectangle_opaque(sample_image, sample_bbox):
    """Test opaque rectangle drawing."""
    result = bbox_visualizer.draw_rectangle(
        sample_image, sample_bbox, is_opaque=True, alpha=0.5
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

def test_add_label(sample_image, sample_bbox, sample_label):
    """Test adding label to bounding box."""
    result = bbox_visualizer.add_label(
        sample_image, sample_label, sample_bbox
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

def test_add_T_label(sample_image, sample_bbox, sample_label):
    """Test adding T-label to bounding box."""
    result = bbox_visualizer.add_T_label(
        sample_image, sample_label, sample_bbox
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

def test_draw_flag_with_label(sample_image, sample_bbox, sample_label):
    """Test drawing flag with label."""
    result = bbox_visualizer.draw_flag_with_label(
        sample_image, sample_label, sample_bbox
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

def test_draw_multiple_rectangles(sample_image):
    """Test drawing multiple rectangles."""
    bboxes = [[10, 10, 30, 30], [40, 40, 60, 60]]
    result = bbox_visualizer.draw_multiple_rectangles(
        sample_image, bboxes
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

def test_add_multiple_labels(sample_image):
    """Test adding multiple labels."""
    bboxes = [[10, 10, 30, 30], [40, 40, 60, 60]]
    labels = ["obj1", "obj2"]
    result = bbox_visualizer.add_multiple_labels(
        sample_image, labels, bboxes
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

def test_add_multiple_T_labels(sample_image):
    """Test adding multiple T-labels."""
    bboxes = [[10, 10, 30, 30], [40, 40, 60, 60]]
    labels = ["obj1", "obj2"]
    # Note: The function internally sets size=1 and thickness=2
    result = bbox_visualizer.add_multiple_T_labels(
        sample_image, labels, bboxes
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

def test_draw_multiple_flags_with_labels(sample_image):
    """Test drawing multiple flags with labels."""
    bboxes = [[10, 10, 30, 30], [40, 40, 60, 60]]
    labels = ["obj1", "obj2"]
    # Note: The function internally sets size=1 and thickness=2
    result = bbox_visualizer.draw_multiple_flags_with_labels(
        sample_image, labels, bboxes
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

def test_invalid_bbox_values(sample_image):
    """Test handling of invalid bbox values."""
    # Testing with invalid bbox coordinates (negative values)
    invalid_bbox = [-10, -10, 20, 20]
    result = bbox_visualizer.draw_rectangle(sample_image, invalid_bbox)
    # The function should handle invalid coordinates by clipping them
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape

def test_empty_inputs():
    """Test handling of empty inputs for multiple object functions."""
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    empty_bboxes = []
    empty_labels = []
    
    # These should handle empty inputs gracefully
    result = bbox_visualizer.draw_multiple_rectangles(img, empty_bboxes)
    assert np.array_equal(result, img)
    
    result = bbox_visualizer.add_multiple_labels(img, empty_labels, empty_bboxes)
    assert np.array_equal(result, img)

def test_color_parameters(sample_image, sample_bbox):
    """Test different color parameters."""
    # Test with different colors
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    for color in colors:
        result = bbox_visualizer.draw_rectangle(
            sample_image, sample_bbox, bbox_color=color
        )
        assert isinstance(result, np.ndarray)
        assert result.shape == sample_image.shape
        assert np.sum(result) > 0 