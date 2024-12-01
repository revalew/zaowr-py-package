import numpy as np
import pytest
from zaowr_polsl_kisiel.calibration import calibrate_camera


@pytest.fixture
def mock_calibrate(mocker):
    mock_glob = mocker.patch("glob.glob", return_value=["/fake/path/image1.png", "/fake/path/image2.png"])
    mock_imread = mocker.patch("cv2.imread", return_value=np.zeros((480, 640, 3), dtype=np.uint8))
    mock_find_corners = mocker.patch("cv2.findChessboardCorners", return_value=(True, np.zeros((70, 1, 2), dtype=np.float32)))
    mock_subpix = mocker.patch("cv2.cornerSubPix", return_value=np.zeros((70, 1, 2), dtype=np.float32))
    mock_calibrate = mocker.patch(
        "cv2.calibrateCamera",
        return_value=(0.5, np.eye(3), np.zeros(5), [np.zeros((3, 1)) for _ in range(2)], [np.zeros((3, 1)) for _ in range(2)]),
    )
    return mock_glob, mock_imread, mock_find_corners, mock_subpix, mock_calibrate

@pytest.mark.parametrize(
    "chessBoardSize, squareRealDimensions, expected_exception",
    [
        ((0, 0), 28.67, ValueError),
        ((10, 7), 0, ValueError),
        ((10, 7), 28.67, None),
    ],
)
def test_calibrate_camera_invalid_params(mock_calibrate, chessBoardSize, squareRealDimensions, expected_exception):
    mock_glob, mock_imread, mock_find_corners, mock_subpix, mock_calibrate = mock_calibrate

    if expected_exception:
        with pytest.raises(expected_exception):
            calibrate_camera(
                chessBoardSize=chessBoardSize,
                squareRealDimensions=squareRealDimensions,
                calibImgDirPath="/fake/path",
                saveCalibrationParams=False
            )
    else:
        calibrate_camera(
            chessBoardSize=chessBoardSize,
            squareRealDimensions=squareRealDimensions,
            calibImgDirPath="/fake/path",
            saveCalibrationParams=False
        )

def test_calibrate_camera_no_images(mock_calibrate, mocker):
    mock_glob, mock_imread, mock_find_corners, mock_subpix, mock_calibrate = mock_calibrate
    mock_glob.return_value = []

    with pytest.raises(Exception, match="Couldn't find any calibration images"):
        calibrate_camera(
            chessBoardSize=(10, 7),
            squareRealDimensions=28.67,
            calibImgDirPath="/empty/path",
            saveCalibrationParams=False
        )

def test_calibrate_camera_no_subpix(mock_calibrate):
    mock_glob, mock_imread, mock_find_corners, mock_subpix, mock_calibrate = mock_calibrate

    calibrate_camera(
        chessBoardSize=(10, 7),
        squareRealDimensions=28.67,
        calibImgDirPath="/fake/path",
        improveSubPix=False,
        saveCalibrationParams=False
    )

    mock_subpix.assert_not_called()

def test_calibrate_camera_display_corners(mock_calibrate, mocker):
    mock_glob, mock_imread, mock_find_corners, mock_subpix, mock_calibrate = mock_calibrate
    mock_show = mocker.patch("cv2.imshow")

    calibrate_camera(
        chessBoardSize=(10, 7),
        squareRealDimensions=28.67,
        calibImgDirPath="/fake/path",
        displayFoundCorners=True,
        saveCalibrationParams=False
    )

    mock_show.assert_called()

def test_calibrate_camera_results(mock_calibrate):
    mock_glob, mock_imread, mock_find_corners, mock_subpix, mock_calibrate = mock_calibrate

    calibrate_camera(
        chessBoardSize=(10, 7),
        squareRealDimensions=28.67,
        calibImgDirPath="/fake/path",
        saveCalibrationParams=False
    )

    mock_calibrate.assert_called()
    rms, cameraMatrix, distortionCoefficients, _, _ = mock_calibrate.return_value
    assert rms == 0.5
    assert cameraMatrix.shape == (3, 3)
    assert len(distortionCoefficients) == 5
