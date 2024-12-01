from unittest.mock import patch

import numpy as np
import pytest
from zaowr_polsl_kisiel.calibration import stereo_calibration
from zaowr_polsl_kisiel.custom_exceptions.exceptions import (
    CalibrationImagesNotFound, CharucoCalibrationError,
)


@pytest.fixture
def mock_stereo_calibration():
    with patch("cv2.imread") as mock_imread, \
         patch("glob.glob") as mock_glob, \
         patch("cv2.findChessboardCorners") as mock_find_corners, \
         patch("cv2.calibrateCamera") as mock_calibrate:
        yield mock_glob, mock_imread, mock_find_corners, mock_calibrate


def test_missing_images(mock_stereo_calibration):
    mock_glob, _, _, _ = mock_stereo_calibration
    mock_glob.side_effect = [[], []]  # Empty directories for left and right cameras

    with pytest.raises(CalibrationImagesNotFound):
        stereo_calibration(
            chessBoardSize=(10, 7),
            squareRealDimensions=50.0,
            calibImgDirPath_left="/fake/path/left",
            calibImgDirPath_right="/fake/path/right"
        )


def test_calibration_results(mock_stereo_calibration):
    mock_glob, mock_imread, mock_find_corners, mock_calibrate = mock_stereo_calibration
    mock_glob.side_effect = [["/fake/path/left/img1.png"], ["/fake/path/right/img1.png"]]
    mock_imread.side_effect = [np.zeros((480, 640, 3), dtype=np.uint8)] * 2
    mock_find_corners.return_value = (True, np.zeros((70, 1, 2), dtype=np.float32))  # Mock corners
    mock_calibrate.side_effect = [  # Mock calibration results
        (0.5, np.eye(3), np.zeros(5), [np.zeros(3)], [np.zeros(3)]),
        (0.5, np.eye(3), np.zeros(5), [np.zeros(3)], [np.zeros(3)])
    ]

    stereo_calibration(
        chessBoardSize=(10, 7),
        squareRealDimensions=50.0,
        calibImgDirPath_left="/fake/path/left",
        calibImgDirPath_right="/fake/path/right",
        displayMSE=True,
    )

    mock_calibrate.assert_called()

def test_invalid_chessboard_size(mock_stereo_calibration):
    with pytest.raises(ValueError, match="Chessboard dimensions must be greater than zero"):
        stereo_calibration(
            chessBoardSize=(0, 0),
            squareRealDimensions=50.0,
            calibImgDirPath_left="/fake/path/left",
            calibImgDirPath_right="/fake/path/right",
        )


def test_corner_detection_failure(mock_stereo_calibration):
    mock_glob, mock_imread, mock_find_corners, _ = mock_stereo_calibration
    mock_glob.side_effect = [["/fake/path/left/img1.png"], ["/fake/path/right/img1.png"]]
    mock_imread.side_effect = [np.zeros((480, 640, 3), dtype=np.uint8)] * 2
    mock_find_corners.side_effect = [(False, None), (False, None)]  # Simulate failure to find corners

    with pytest.raises(CharucoCalibrationError, match="Error during ChArUco board calibration"):
        stereo_calibration(
            chessBoardSize=(10, 7),
            squareRealDimensions=50.0,
            calibImgDirPath_left="/fake/path/left",
            calibImgDirPath_right="/fake/path/right",
            useCharuco=True,
        )
