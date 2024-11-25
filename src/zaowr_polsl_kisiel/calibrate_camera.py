from typing import TYPE_CHECKING, Any, TypedDict
import numpy as np
import cv2 as cv
import glob
from .exceptions import CalibrationImagesNotFound, CalibrationParamsPathNotProvided, CalibrationParamsWrongFormat

# To avoid creating a class at runtime, for type-hinting alone.
if TYPE_CHECKING:
    # Map the `dict` fields here
    class CalibrationParams(TypedDict):
        mse: float
        rms: float
        objPoints: Any
        imgPoints: Any
        cameraMatrix: Any
        distortionCoefficients: Any
        rotationVectors: Any
        translationVectors: Any


def calibrate_camera(
    chessBoardSize: tuple[int, int],
    squareRealDimensions: float,
    calibImgDirPath: str,
    globImgExtension: str = "png",
    saveCalibrationParams: bool = False,
    loadCalibrationParams: bool = False,
    calibrationParamsPath: str = "",
    displayFoundCorners: bool = False,
    displayMSE: bool = False,
    improveSubPix: bool = True,
    showListOfImagesWithChessboardFound: bool = False,
    terminationCriteria: tuple[Any, int, float] = (
        cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER,
        30,
        0.001,
    ),
) -> None | CalibrationParams:
    """
    Calibrate the camera using the provided chessboard images. Can also be used to load calibration parameters saved in a JSON file.

    :param tuple[int, int] chessBoardSize: Size of the chessboard (corners between two sides of the chessboard) passed as a tuple. First value has to be the WIDTH, and the second value has to be the HEIGHT, e.g.
        Chessboard in the OpenCV documentation `https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html` has dimensions (6, 9).
    :param float squareRealDimensions: Real dimensions of the squares on the chessboard, e.g. one square is exactly 28.67mmx28.67mm. Pass ONLY ONE argument - "28.67".
    :param str calibImgDirPath: Path to the directory containing images with chessboards.
    :param str globImgExtension: Extension of the chessboard images ("jpg" or "png"), defaults to "png"
    :param bool saveCalibrationParams: Decide if you want to save the parameters calculated during the calibration process, defaults to False
    :param bool loadCalibrationParams: Decide if you want to load the parameters calculated during the calibration process, defaults to False
    :param str calibrationParamsPath: Path where we want to save the calibration parameters, defaults to ""
    :param bool displayFoundCorners: Decide if you want to display the calibration images with marked corners found by cv2, defaults to False
    :param bool displayMSE: Decide if you want to print the MSE of each image during calibration, defaults to False
    :param bool improveSubPix: Decide if you want to refine the corners found in the calibration images with sub-pixel precision, defaults to True
    :param bool showListOfImagesWithChessboardFound: Decide if you want to show the list of images with chessboard found, defaults to False
    :param tuple[Any, int, float] terminationCriteria: Specify the termination criteria for the process of finding square corners in the sub-pixels, defaults to ( cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    :return: None | CalibrationParams dict[str, Any] - Returns calibration parameters of the camera in form of a dict:
        - **mse** - Mean Square Error,
        - **rms** - The overall RMS re-projection error in floating number format,
        - **objPoints** - 3D point in real world space,
        - **imgPoints** - 2D points in image plane,
        - **cameraMatrix** - Camera Matrix, the focal length and optical centre matrix as shown in intrinsic parameters,
        - **distortionCoefficients** - Distortion Coefficients: (k<sub>1</sub>, k<sub>2</sub>, p<sub>1</sub>, p<sub>2</sub>, k<sub>3</sub>), which include radial (k<sub>n</sub>) and tangential (p<sub>n</sub>) distortion values,
        - **rotationVectors** - Rotation Vector, the image pixel rotation angles in radians converted to vector by Rodrigues method,
        - **translationVectors** - Translation Vector, the vector depicting shift in pixel values along x and y axis.

    :raises CalibrationImagesNotFound: Raises an error if the calibration images could not be found in the given path.
    """

    if not loadCalibrationParams:
        ######################################################################################
        # Calibrate camera
        ######################################################################################
        # termination criteria for images
        # terminationCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        # objp = np.zeros((10 * 7, 3), np.float32)
        # objp[:, :2] = np.mgrid[0:10, 0:7].T.reshape(-1, 2) * 28.67
        objP = np.zeros((chessBoardSize[0] * chessBoardSize[1], 3), np.float32)
        objP[:, :2] = (
            np.mgrid[0 : chessBoardSize[0], 0 : chessBoardSize[1]].T.reshape(-1, 2)
            * squareRealDimensions
        )

        # Arrays to store object points and image points from all the images.
        objPoints = []  # 3d point in real world space
        imgPoints = []  # 2d points in image plane.

        # e.g. "../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/*.png"
        images = glob.glob(calibImgDirPath + "/*." + globImgExtension)
        chessboardFound = [] # list of images with chessboard detected properly

        if (images == []) or (len(images) == 0):
            raise CalibrationImagesNotFound

        for fileName in images:
            img = cv.imread(fileName)
            grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners1 = cv.findChessboardCorners(
                grayImg, (chessBoardSize[0], chessBoardSize[1]), None
            )

            # If found, add object points, image points (after refining them)
            if ret == True:
                chessboardFound.append(fileName)
                objPoints.append(objP)

                if improveSubPix:
                    corners2 = cv.cornerSubPix(
                        grayImg, corners1, (11, 11), (-1, -1), terminationCriteria
                    )
                    imgPoints.append(corners2)

                else:
                    imgPoints.append(corners1)

                if displayFoundCorners:
                    # Draw and display the corners
                    # cv.drawChessboardCorners(img, (10, 7), corners2, ret)
                    cv.drawChessboardCorners(
                        img, (chessBoardSize[0], chessBoardSize[1]), corners2, ret
                    )
                    cv.imshow("Current Image", img)
                    cv.waitKey(500)

        cv.destroyAllWindows()

        if showListOfImagesWithChessboardFound:
            print("\nList of images with chessboard found:\n")
            print(chessboardFound)

        # overall RMS re-projection error, camera matrix, distortion coefficients, rotation vectors, translation vectors
        rms, cameraMatrix, distortionCoefficients, rotationVectors, translationVectors = (
            cv.calibrateCamera(objPoints, imgPoints, grayImg.shape[::-1], None, None)
        )

        mse = 0
        for i in range(len(objPoints)):
            imgPoints2, _ = cv.projectPoints(
                objPoints[i],
                rotationVectors[i],
                translationVectors[i],
                cameraMatrix,
                distortionCoefficients,
            )
            error = cv.norm(imgPoints[i], imgPoints2, cv.NORM_L2) / len(imgPoints2)
            mse += error
        if displayMSE:
            print("\nMean reprojection error: {}", mse / len(objPoints))

        if saveCalibrationParams:
            try:
                from .save_calibration import save_calibration

                calibrationParams = {
                    "mse": mse,
                    "rms": rms,
                    "objPoints": objPoints,
                    "imgPoints": imgPoints,
                    "cameraMatrix": cameraMatrix.tolist(),
                    "distortionCoefficients": distortionCoefficients.tolist(),
                    "rotationVectors": [rvec.tolist() for rvec in rotationVectors],
                    "translationVectors": [tvec.tolist() for tvec in translationVectors],
                }

                save_calibration(calibrationParams, calibrationParamsPath)

            except CalibrationParamsPathNotProvided:
                print("\nError occurred while saving the calibration parameters!\n")
                raise

            except Exception as e:
                print("\nUnknown error occurred\n")
                raise

    else:
        ######################################################################################
        # Load calibration
        ######################################################################################
        try:
            from .load_calibration import load_calibration

            calibrationParams = load_calibration(calibrationParamsPath)

            # mse = calibrationParams["mse"]
            # rms = calibrationParams["rms"]
            # objPoints = calibrationParams["objPoints"]
            # imgPoints = calibrationParams["imgPoints"]
            # cameraMatrix = calibrationParams["cameraMatrix"]
            # distortionCoefficients = calibrationParams["distortionCoefficients"]
            # rotationVectors = calibrationParams["rotationVectors"]
            # translationVectors = calibrationParams["translationVectors"]

            return calibrationParams

        except CalibrationParamsPathNotProvided:
            print("\nError occurred while loading the calibration parameters!\n")
            raise

        except CalibrationParamsWrongFormat:
            print("\nCalibration parameters are not in the correct format!\n")
            raise

        except Exception as e:
            print("\nUnknown error occurred\n")
            raise

