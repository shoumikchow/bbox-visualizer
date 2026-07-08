import logging

import numpy as np
import pytest

from bbox_visualizer.core import flags, labels, rectangle
from bbox_visualizer.core._utils import _convert_bbox_to_voc, _get_text_size


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


def test_draw_box_basic(sample_image, sample_bbox):
    """Test basic box drawing functionality."""
    result = rectangle.draw_box(sample_image, sample_bbox)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    # Check if box was drawn (should have some non-zero pixels)
    assert np.sum(result) > 0


def test_draw_box_opaque(sample_image, sample_bbox):
    """Test opaque box drawing."""
    result = rectangle.draw_box(sample_image, sample_bbox, is_opaque=True, alpha=0.5)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0


def test_draw_box_aliases(sample_image, sample_bbox):
    """Test that draw_rectangle and draw_box are aliases."""
    assert rectangle.draw_box is rectangle.draw_rectangle
    assert rectangle.draw_multiple_boxes is rectangle.draw_multiple_rectangles


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

    # Test with draw_bg=False for both top and bottom positions.
    # Default text color is black, invisible on the black test image,
    # so use white to verify something was drawn.
    result = labels.add_label(
        sample_image,
        sample_label,
        bbox_with_space,
        draw_bg=False,
        text_color=(255, 255, 255),
        top=True,
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0

    result = labels.add_label(
        sample_image,
        sample_label,
        bbox_with_space,
        draw_bg=False,
        text_color=(255, 255, 255),
        top=False,
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


def test_label_bg_contains_text_at_size_2():
    """Flag and T-label background rects fully contain the text at size=2."""
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    red, green = (0, 0, 255), (0, 255, 0)

    # "py" has descenders, which must also stay inside the bg
    flag = flags.draw_flag_with_label(
        img,
        "py",
        [50, 150, 250, 290],
        size=2,
        thickness=2,
        line_color=red,
        text_bg_color=red,
        text_color=green,
    )
    t_label = flags.add_T_label(
        img,
        "py",
        [100, 200, 200, 290],
        size=2,
        thickness=2,
        text_bg_color=red,
        text_color=green,
    )
    for result in (flag, t_label):
        text = np.argwhere((result == green).all(axis=2))
        bg = np.argwhere((result == red).all(axis=2))
        assert len(text) > 0
        assert text[:, 0].min() >= bg[:, 0].min()
        assert text[:, 0].max() <= bg[:, 0].max()
        assert text[:, 1].min() >= bg[:, 1].min()
        assert text[:, 1].max() <= bg[:, 1].max()


def test_fallback_uses_caller_styling(sample_image, sample_label):
    """Fallback to normal labeling keeps the caller's colors."""
    blue = (255, 0, 0)
    t_result = flags.add_T_label(
        sample_image, sample_label, [10, 5, 50, 20], text_bg_color=blue
    )
    flag_result = flags.draw_flag_with_label(
        sample_image, sample_label, [10, 0, 50, 10], text_bg_color=blue
    )
    for result in (t_result, flag_result):
        assert (result == blue).all(axis=2).any()


def test_draw_multiple_boxes(sample_image):
    """Test drawing multiple boxes."""
    bboxes = [[10, 10, 30, 30], [50, 50, 70, 70]]
    result = rectangle.draw_multiple_boxes(sample_image, bboxes)
    assert isinstance(result, np.ndarray)
    assert result.shape == sample_image.shape
    assert np.sum(result) > 0


def test_draw_multiple_boxes_per_box_colors(sample_image):
    """A sequence of colors draws each box in its own color."""
    bboxes = [[10, 10, 30, 30], [50, 50, 70, 70]]
    colors = [(255, 0, 0), (0, 255, 0)]
    result = rectangle.draw_multiple_rectangles(sample_image, bboxes, colors)
    for color in colors:
        assert (result == color).all(axis=2).any()


def test_draw_multiple_boxes_color_length_mismatch(sample_image):
    """Color list length must match the number of boxes."""
    bboxes = [[10, 10, 30, 30], [50, 50, 70, 70]]
    with pytest.raises(ValueError, match="must match"):
        rectangle.draw_multiple_rectangles(sample_image, bboxes, [(255, 0, 0)])


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
        rectangle.draw_box(sample_image, [])

    # Test with invalid bbox format
    with pytest.raises(ValueError):
        rectangle.draw_box(sample_image, [1, 2, 3])  # Missing one coordinate

    # Test with invalid coordinate order (x_min > x_max or y_min > y_max)
    with pytest.raises(ValueError):
        rectangle.draw_box(sample_image, [50, 10, 10, 50])  # x_min > x_max
    with pytest.raises(ValueError):
        rectangle.draw_box(sample_image, [10, 50, 50, 10])  # y_min > y_max


def test_empty_inputs():
    """Test handling of empty inputs for multiple object functions."""
    img = np.zeros((100, 100, 3), dtype=np.uint8)

    # Test with empty lists
    with pytest.raises(ValueError):
        rectangle.draw_multiple_boxes(img, [])
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
        rectangle.draw_box(
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

    # Colors may be any 3-length sequence, not just tuples
    result = labels.add_label(sample_image, "test", sample_bbox, text_color=[0, 255, 0])
    assert isinstance(result, np.ndarray)


def test_convert_bbox_to_voc(sample_image):
    """Test conversion of COCO and YOLO formats to Pascal VOC."""
    img_shape = sample_image.shape  # (100, 100, 3)

    # VOC passes through unchanged
    assert _convert_bbox_to_voc([10, 10, 50, 50], img_shape, "voc") == [10, 10, 50, 50]

    # COCO [x_min, y_min, width, height] -> VOC
    assert _convert_bbox_to_voc([10, 10, 40, 40], img_shape, "coco") == [10, 10, 50, 50]

    # YOLO [x_center, y_center, width, height] normalized -> VOC
    assert _convert_bbox_to_voc([0.3, 0.3, 0.4, 0.4], img_shape, "yolo") == [
        10,
        10,
        50,
        50,
    ]

    # Format string is case-insensitive
    assert _convert_bbox_to_voc([10, 10, 40, 40], img_shape, "COCO") == [10, 10, 50, 50]


def test_convert_bbox_to_voc_invalid(sample_image):
    """Test invalid arguments to the format conversion helper."""
    img_shape = sample_image.shape

    # Unsupported format
    with pytest.raises(ValueError):
        _convert_bbox_to_voc([10, 10, 50, 50], img_shape, "albumentations")

    # Wrong number of coordinates
    with pytest.raises(ValueError):
        _convert_bbox_to_voc([10, 10, 50], img_shape, "coco")

    # Negative width/height
    with pytest.raises(ValueError):
        _convert_bbox_to_voc([10, 10, -5, 40], img_shape, "coco")
    with pytest.raises(ValueError):
        _convert_bbox_to_voc([0.3, 0.3, -0.4, 0.4], img_shape, "yolo")


def test_bbox_format_kwarg_equivalence(sample_image, sample_label):
    """COCO and YOLO inputs should render identically to their VOC equivalent."""
    voc = [10, 10, 50, 50]
    coco = [10, 10, 40, 40]
    yolo = [0.3, 0.3, 0.4, 0.4]

    # draw_box
    expected = rectangle.draw_box(sample_image, voc)
    assert np.array_equal(
        rectangle.draw_box(sample_image, coco, bbox_format="coco"), expected
    )
    assert np.array_equal(
        rectangle.draw_box(sample_image, yolo, bbox_format="yolo"), expected
    )

    # add_label
    expected = labels.add_label(sample_image, sample_label, voc)
    assert np.array_equal(
        labels.add_label(sample_image, sample_label, coco, bbox_format="coco"),
        expected,
    )
    assert np.array_equal(
        labels.add_label(sample_image, sample_label, yolo, bbox_format="yolo"),
        expected,
    )


def test_bbox_format_kwarg_multiple(sample_image):
    """Multiple-object functions should accept the bbox_format kwarg."""
    coco_bboxes = [[10, 10, 20, 20], [50, 50, 20, 20]]
    voc_bboxes = [[10, 10, 30, 30], [50, 50, 70, 70]]
    labels_list = ["obj1", "obj2"]

    expected = rectangle.draw_multiple_boxes(sample_image, voc_bboxes)
    result = rectangle.draw_multiple_boxes(
        sample_image, coco_bboxes, bbox_format="coco"
    )
    assert np.array_equal(result, expected)

    # Smoke-test the remaining multi-object functions with the kwarg
    assert isinstance(
        labels.add_multiple_labels(
            sample_image, labels_list, coco_bboxes, bbox_format="coco"
        ),
        np.ndarray,
    )
    assert isinstance(
        flags.add_multiple_T_labels(
            sample_image, labels_list, coco_bboxes, bbox_format="coco"
        ),
        np.ndarray,
    )
    assert isinstance(
        flags.draw_multiple_flags_with_labels(
            sample_image, labels_list, coco_bboxes, bbox_format="coco"
        ),
        np.ndarray,
    )


@pytest.mark.parametrize(
    "func",
    [
        lambda img: rectangle.draw_rectangle(img, [10, 30, 50, 70]),
        lambda img: rectangle.draw_rectangle(img, [10, 30, 50, 70], is_opaque=True),
        lambda img: rectangle.draw_multiple_rectangles(
            img, [[10, 30, 50, 70], [20, 40, 60, 80]]
        ),
        lambda img: labels.add_label(img, "test", [10, 30, 50, 70]),
        lambda img: labels.add_label(img, "test", [10, 5, 50, 20]),  # fallback: inside
        lambda img: labels.add_multiple_labels(
            img, ["a", "b"], [[10, 30, 50, 70], [20, 40, 60, 80]]
        ),
        lambda img: flags.add_T_label(img, "test", [40, 80, 60, 95]),
        lambda img: flags.add_T_label(img, "test", [10, 5, 50, 20]),  # fallback
        lambda img: flags.add_multiple_T_labels(
            img, ["a", "b"], [[40, 80, 60, 95], [20, 80, 40, 95]]
        ),
        lambda img: flags.draw_flag_with_label(img, "test", [10, 30, 50, 70]),
        lambda img: flags.draw_flag_with_label(
            img, "test", [10, 0, 50, 10]
        ),  # fallback
        lambda img: flags.draw_multiple_flags_with_labels(
            img, ["a", "b"], [[10, 30, 50, 70], [20, 40, 60, 80]]
        ),
    ],
)
def test_input_image_not_modified(sample_image, func):
    """All public functions must return a new image and leave the input untouched."""
    before = sample_image.copy()
    result = func(sample_image)
    assert np.array_equal(sample_image, before)
    assert result is not sample_image


def test_fallback_warning_uses_module_logger(sample_image, sample_label, caplog):
    """Fallback warning is emitted on the flags logger and silenced via logging."""
    with caplog.at_level(logging.WARNING):
        flags.draw_flag_with_label(sample_image, sample_label, [10, 0, 50, 10])
    assert any(
        r.name == "bbox_visualizer.core.flags"
        and "Labelling style 'Flag' going out of frame" in r.message
        for r in caplog.records
    )

    caplog.clear()
    logging.getLogger("bbox_visualizer").setLevel(logging.ERROR)
    try:
        with caplog.at_level(logging.WARNING):
            flags.draw_flag_with_label(sample_image, sample_label, [10, 0, 50, 10])
        assert len(caplog.records) == 0
    finally:
        logging.getLogger("bbox_visualizer").setLevel(logging.NOTSET)


def test_numpy_array_bboxes(sample_image):
    """A numpy array of boxes works everywhere a list of boxes does."""
    bboxes = np.array([[10, 10, 30, 30], [50, 50, 70, 70]])
    names = ["a", "b"]
    rectangle.draw_multiple_rectangles(sample_image, bboxes)
    labels.add_multiple_labels(sample_image, names, bboxes)
    flags.add_multiple_T_labels(sample_image, names, bboxes)
    flags.draw_multiple_flags_with_labels(sample_image, names, bboxes)


def test_numpy_integer_color(sample_image, sample_bbox):
    """Colors made of numpy integer scalars (e.g. sampled pixels) are valid."""
    color = tuple(np.uint8(c) for c in (255, 0, 0))
    result = rectangle.draw_rectangle(sample_image, sample_bbox, bbox_color=color)
    assert (result == (255, 0, 0)).all(axis=2).any()


def test_label_falls_back_inside_when_bg_does_not_fit_above(sample_image):
    """The label goes inside the box when the full background can't fit above."""
    (_, text_height), baseline = _get_text_size("test", 0.3, 1)
    bg_height = text_height + baseline + 2 * 5  # mirrors add_label's padding
    y_min = bg_height - 1  # one pixel short of fitting the background above
    result = labels.add_label(
        sample_image, "test", [10, y_min, 90, 90], size=0.3, thickness=1
    )
    assert not result[:y_min].any()
