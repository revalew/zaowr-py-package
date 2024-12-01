import pytest
from unittest.mock import MagicMock, patch
import numpy as np
from zaowr_polsl_kisiel.image_processing import stereo_rectify
from zaowr_polsl_kisiel.custom_exceptions.exceptions import (
    CalibrationImagesNotFound,
    MissingParameters,
    StereoRectificationError,
)


@pytest.fixture
def mock_stereo_rectify():
    """
    Fixture to mock dependencies in the stereo_rectify function.
    """
    mock_imread = MagicMock()
    mock_glob = MagicMock()
    mock_rectify_map = MagicMock()
    mock_remap = MagicMock()
    mock_line = MagicMock()
    mock_imwrite = MagicMock()

    with patch("cv2.imread", mock_imread), \
         patch("cv2.initUndistortRectifyMap", mock_rectify_map), \
         patch("cv2.remap", mock_remap), \
         patch("cv2.line", mock_line), \
         patch("cv2.imwrite", mock_imwrite), \
         patch("glob.glob", mock_glob):
        yield mock_imread, mock_glob, mock_rectify_map, mock_remap, mock_line, mock_imwrite


def test_missing_images(mock_stereo_rectify):
    mock_imread, mock_glob, *_ = mock_stereo_rectify
    mock_glob.side_effect = [[], []]  # Simulate no images found

    with pytest.raises(CalibrationImagesNotFound, match="Couldn't find any calibration images"):
        stereo_rectify(
            calibImgDirPath_left="/fake/path/left",
            calibImgDirPath_right="/fake/path/right",
            rectifiedImagesDirPath="/fake/output",
        )



def test_missing_parameters(mock_stereo_rectify):
    """
    Test that MissingParameters is raised if required parameters are missing.
    """
    mock_imread, mock_glob, *_ = mock_stereo_rectify
    mock_glob.side_effect = [["/fake/path/left/img1.png"], ["/fake/path/right/img1.png"]]
    mock_imread.side_effect = [np.zeros((480, 640, 3), dtype=np.uint8)] * 2

    with pytest.raises(MissingParameters, match="Some parameters are missing"):
        stereo_rectify(
            calibImgDirPath_left="/fake/path/left",
            calibImgDirPath_right="/fake/path/right",
            rectifiedImagesDirPath="/fake/output",
            cameraMatrix_left=None,  # Parameters missing
        )


def test_successful_rectification(mock_stereo_rectify):
    mock_imread, mock_glob, mock_rectify_map, mock_remap, mock_line, mock_imwrite = mock_stereo_rectify
    mock_glob.side_effect = [["/fake/path/left/img1.png"], ["/fake/path/right/img1.png"]]
    mock_imread.side_effect = iter([np.zeros((480, 640, 3), dtype=np.uint8)] * 4)

    mock_rectify_map.return_value = (np.zeros((480, 640), dtype=np.float32), np.zeros((480, 640), dtype=np.float32))
    mock_remap.side_effect = [np.zeros((480, 640, 3), dtype=np.uint8)] * 2

    with patch("os.makedirs") as mock_makedirs:
        stereo_rectify(
            calibImgDirPath_left="/fake/path/left",
            calibImgDirPath_right="/fake/path/right",
            rectifiedImagesDirPath="/fake/output",
            imgPoints_left=np.eye(3, dtype=np.float64),
            imgPoints_right=np.eye(3, dtype=np.float64),
            cameraMatrix_left=np.eye(3, dtype=np.float64),
            cameraMatrix_right=np.eye(3, dtype=np.float64),
            distortionCoefficients_left=np.zeros(5),
            distortionCoefficients_right=np.zeros(5),
            R=np.eye(3, dtype=np.float64),
            T=np.array([1, 0, 0], dtype=np.float64),
            F=np.eye(3, dtype=np.float64),
            saveRectifiedImages=True,
        )
        mock_makedirs.assert_called_once_with("/fake/output")
    mock_imwrite.assert_called()



def test_invalid_rectification_maps(mock_stereo_rectify):
    mock_imread, mock_glob, mock_rectify_map, *_ = mock_stereo_rectify
    mock_glob.side_effect = [["/fake/path/left/img1.png"], ["/fake/path/right/img1.png"]]
    mock_imread.side_effect = [np.zeros((480, 640, 3), dtype=np.uint8)] * 2
    mock_rectify_map.side_effect = Exception("Error in stereo rectification process")

    with pytest.raises(StereoRectificationError, match="Error in stereo rectification process"):
        stereo_rectify(
            calibImgDirPath_left="/fake/path/left",
            calibImgDirPath_right="/fake/path/right",
            rectifiedImagesDirPath="/fake/output",
            cameraMatrix_left=np.eye(3),
            cameraMatrix_right=np.eye(3),
            distortionCoefficients_left=np.zeros(5),
            distortionCoefficients_right=np.zeros(5),
            R=np.eye(3),
            T=np.array([1, 0, 0]),
        )


def test_invalid_image_shapes(mock_stereo_rectify):
    mock_imread, mock_glob, *_ = mock_stereo_rectify
    mock_glob.side_effect = [["/fake/path/left/img1.png"], ["/fake/path/right/img1.png"]]
    mock_imread.side_effect = [
        np.zeros((480, 640, 3), dtype=np.uint8),
        np.zeros((400, 600, 3), dtype=np.uint8),
    ]

    with pytest.raises(StereoRectificationError, match="Error in stereo rectification process"):
        stereo_rectify(
            calibImgDirPath_left="/fake/path/left",
            calibImgDirPath_right="/fake/path/right",
            rectifiedImagesDirPath="/fake/output",
            cameraMatrix_left=np.eye(3),
            cameraMatrix_right=np.eye(3),
            distortionCoefficients_left=np.zeros(5),
            distortionCoefficients_right=np.zeros(5),
            R=np.eye(3),
            T=np.array([1, 0, 0]),
        )

