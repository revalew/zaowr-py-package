class CalibrationImagesNotFound(Exception):
    """
    Couldn't find any calibration images in given path!\nProvide appropriate path and re-run the program.
    """

    def __init__(
        self,
        message="Couldn't find any calibration images in given path!\nProvide appropriate path and re-run the program.",
    ):
        self.message = message
        super().__init__(self.message)


class CalibrationParamsPathNotProvided(Exception):
    """
    Path to the calibration file was not provided or it is not a string!\nProvide appropriate path and re-run the program.
    """

    def __init__(
        self,
        message="Path to the calibration file was not provided or it is not a string!\nProvide appropriate path and re-run the program.",
    ):
        self.message = message
        super().__init__(self.message)

class StereoCalibrationParamsPathNotProvided(Exception):
    """
    Path to the stereo calibration file was not provided or it is not a string!\nProvide appropriate path and re-run the program.
    """

    def __init__(
        self,
        message="Path to the stereo calibration file was not provided or it is not a string!\nProvide appropriate path and re-run the program.",
    ):
        self.message = message
        super().__init__(self.message)

class CalibrationParamsWrongFormat(Exception):
    """
    Provided file contains wrong params with wrong format or empty fields.
    """

    def __init__(
        self,
        message="Provided file contains wrong params with wrong format or empty fields.",
    ):
        self.message = message
        super().__init__(self.message)


class ImgToUndistortPathNotProvided(Exception):
    """
    Path to the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program.
    """

    def __init__(
        self,
        message="Path to the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program.",
    ):
        self.message = message
        super().__init__(self.message)


class UndistortedImgPathNotProvided(Exception):
    """
    Path to save the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program.
    """

    def __init__(
        self,
        message="Path to save the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program.",
    ):
        self.message = message
        super().__init__(self.message)

class RectifiedImgPathNotProvided(Exception):
    """
    Path to save the rectified image was not provided or it is not a string!\nProvide appropriate path and re-run the program.
    """

    def __init__(
        self,
        message="Path to save the rectified image was not provided or it is not a string!\nProvide appropriate path and re-run the program.",
    ):
        self.message = message
        super().__init__(self.message)

class MissingParameters(Exception):
    """
    Some parameters are missing in the function call.
    """

    def __init__(
        self,
        message="Some parameters are missing in the function call.",
    ):
        self.message = message
        super().__init__(self.message)

class RectificationMapsPathNotProvided(Exception):
    """
    Path to the rectification maps file was not provided or it is not a string!\nProvide appropriate path and re-run the program.
    """

    def __init__(
        self,
        message="Path to the rectification maps file was not provided or it is not a string!\nProvide appropriate path and re-run the program.",
    ):
        self.message = message
        super().__init__(self.message)

class CharucoCalibrationError(Exception):
    """
    Error during ChArUco board calibration.
    """

    def __init__(
        self,
        message="Error during ChArUco board calibration. Ensure the images and parameters are correct, especially the board size.",
    ):
        self.message = message
        super().__init__(self.message)