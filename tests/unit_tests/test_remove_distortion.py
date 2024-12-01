import numpy as np
import pytest
from zaowr_polsl_kisiel.custom_exceptions.exceptions import ImgToUndistortPathNotProvided, UndistortedImgPathNotProvided
from zaowr_polsl_kisiel.image_processing import remove_distortion


@pytest.fixture
def mock_remove_distortion(mocker):
    # Mock cv2.imread to return a fake image
    mock_imread = mocker.patch("cv2.imread", return_value=np.zeros((480, 640, 3), dtype=np.uint8))
    # Mock cv2.imshow to avoid GUI interaction
    mock_imshow = mocker.patch("cv2.imshow")
    # Mock cv2.imwrite to avoid actual file creation
    mock_imwrite = mocker.patch("cv2.imwrite")
    # Mock os.makedirs to avoid directory creation
    mock_makedirs = mocker.patch("os.makedirs")
    return mock_imread, mock_imshow, mock_imwrite, mock_makedirs

def test_remove_distortion_missing_img_path(mock_remove_distortion):
    mock_imread, _, _, _ = mock_remove_distortion
    with pytest.raises(ImgToUndistortPathNotProvided):
        remove_distortion(
            cameraMatrix=np.eye(3),
            distortionCoefficients=np.zeros(5),
            imgToUndistortPath="",
        )

def test_remove_distortion_save_without_path(mock_remove_distortion):
    mock_imread, _, _, _ = mock_remove_distortion
    with pytest.raises(UndistortedImgPathNotProvided):
        remove_distortion(
            cameraMatrix=np.eye(3),
            distortionCoefficients=np.zeros(5),
            imgToUndistortPath="/fake/image.png",
            saveUndistortedImg=True,
            undistortedImgPath="",
        )

def test_remove_distortion_undistort_method(mock_remove_distortion):
    mock_imread, mock_imshow, _, _ = mock_remove_distortion
    remove_distortion(
        cameraMatrix=np.eye(3),
        distortionCoefficients=np.zeros(5),
        imgToUndistortPath="/fake/image.png",
        undistortionMethod="undistort",
        showUndistortedImg=True,
    )
    mock_imread.assert_called_with("/fake/image.png")
    assert mock_imshow.call_count == 1

def test_remove_distortion_remapping_method(mock_remove_distortion):
    mock_imread, mock_imshow, _, _ = mock_remove_distortion
    remove_distortion(
        cameraMatrix=np.eye(3),
        distortionCoefficients=np.zeros(5),
        imgToUndistortPath="/fake/image.png",
        undistortionMethod="remapping",
        showUndistortedImg=True,
    )
    mock_imread.assert_called_with("/fake/image.png")
    assert mock_imshow.call_count == 1


def test_remove_distortion_save_image(mock_remove_distortion):
    mock_imread, _, mock_imwrite, mock_makedirs = mock_remove_distortion
    remove_distortion(
        cameraMatrix=np.eye(3),
        distortionCoefficients=np.zeros(5),
        imgToUndistortPath="/fake/image.png",
        saveUndistortedImg=True,
        undistortedImgPath="/fake/output/",
    )
    mock_imread.assert_called_with("/fake/image.png")
    mock_makedirs.assert_called_with("/fake/output/", exist_ok=True)
    mock_imwrite.assert_called()


def test_remove_distortion_invalid_method(mock_remove_distortion):
    mock_imread, _, _, _ = mock_remove_distortion
    with pytest.raises(ValueError, match="Invalid undistortion method"):
        remove_distortion(
            cameraMatrix=np.eye(3),
            distortionCoefficients=np.zeros(5),
            imgToUndistortPath="/fake/image.png",
            undistortionMethod="invalid_method",
        )