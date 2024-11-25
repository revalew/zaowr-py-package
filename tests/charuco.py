from typing import TYPE_CHECKING, Any, TypedDict
import numpy as np
import cv2 as cv
from cv2 import aruco
import glob
from .exceptions import CalibrationImagesNotFound, CalibrationParamsPathNotProvided, CalibrationParamsWrongFormat, CharucoCalibrationError


def calibrate_camera(
    chessBoardSize: tuple[int, int],
    squareRealDimensions: float,
    calibImgDirPath: str,
    globImgExtension: str = "png",
    saveCalibrationParams: bool = False,
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
    useCharuco: bool = False,
    arucoDictName: str = "DICT_6X6_250",
    markerLength: float = 20.0,
) -> None:
    """
    Calibrate the camera using the provided chessboard images or ChArUco board images. Can also be used to load calibration parameters saved in a JSON file.

    :param tuple[int, int] chessBoardSize: Size of the chessboard (corners between two sides of the chessboard) passed as a tuple. First value has to be the WIDTH, and the second value has to be the HEIGHT, e.g.
        Chessboard in the OpenCV documentation `https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html` has dimensions (6, 9).
    :param float squareRealDimensions: Real dimensions of the squares on the chessboard, e.g. one square is exactly 28.67mmx28.67mm. Pass ONLY ONE argument - "28.67".
    :param str calibImgDirPath: Path to the directory containing images with chessboards.
    :param str globImgExtension: Extension of the chessboard images ("jpg" or "png"), defaults to "png"
    :param bool saveCalibrationParams: Decide if you want to save the parameters calculated during the calibration process, defaults to False
    :param str calibrationParamsPath: Path where we want to save the calibration parameters, defaults to ""
    :param bool displayFoundCorners: Decide if you want to display the calibration images with marked corners found by cv2, defaults to False
    :param bool displayMSE: Decide if you want to print the MSE of each image during calibration, defaults to False
    :param bool improveSubPix: Decide if you want to refine the corners found in the calibration images with sub-pixel precision, defaults to True
    :param bool showListOfImagesWithChessboardFound: Decide if you want to show the list of images with chessboard found, defaults to False
    :param tuple[Any, int, float] terminationCriteria: Specify the termination criteria for the process of finding square corners in the sub-pixels, defaults to ( cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    :return: None

    :raises CalibrationImagesNotFound: Raises an error if the calibration images could not be found in the given path.
    """
    # e.g. "../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/*.png"
    images = glob.glob(calibImgDirPath + "/*." + globImgExtension)

    if (images == []) or (len(images) == 0):
        raise CalibrationImagesNotFound

    if useCharuco:
        try:
            arucoDict = getattr(aruco, arucoDictName)
            dictionary = aruco.getPredefinedDictionary(arucoDict)
            board = aruco.CharucoBoard(chessBoardSize, squareRealDimensions, markerLength, dictionary)
            params = aruco.DetectorParameters()
            charucodetector = aruco.CharucoDetector(board, params)

            objPoints = []  # 3D points in real world space
            imgPoints = []  # 2D points in image plane
            imgSize = None
            chessboardFound = []

            for fileName in images:
                img = cv.imread(fileName)
                grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                # corners, ids, _ = aruco.detectMarkers(grayImg, dictionary)

                # charuco_corners, charuco_ids, marker_corners, marker_ids = charucodetector.detectBoard(image)
                charucoCorners, charucoIds, corners, ids = charucodetector.detectBoard(grayImg)
                # corners, ids, charucoCorners, charucoIds = charucodetector.detectBoard(grayImg)

                if (ids is not None) and (len(ids) > 0):
                    if improveSubPix:
                        corners = [
                            cv.cornerSubPix(
                                grayImg, cornerSet, (11, 11), (-1, -1), terminationCriteria
                            )
                            for cornerSet in corners
                        ]

                    if displayFoundCorners:
                        imgWithMarkers = aruco.drawDetectedMarkers(img, corners, ids)
                        cv.imshow("Detected ChArUco Markers", imgWithMarkers)
                        cv.waitKey(500)

                    if corners:
                        # print("Found chessboard")
                        chessboardFound.append(fileName)
                        objPoints.append(ids)
                        imgPoints.append(corners)

                        if imgSize is None:
                            imgSize = grayImg.shape[::-1]

            if len(objPoints) < 1:
                raise CharucoCalibrationError

            rms, cameraMatrix, distortionCoefficients, rotationVectors, translationVectors = aruco.calibrateCameraCharuco(
                imgPoints, objPoints, board, imgSize, None, None
            )

            # rms, cameraMatrix, distortionCoefficients, rotationVectors, translationVectors = aruco.calibrateCameraCharuco(
            #     corners, ids, board, imgSize, None, None
            # )

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
                        "mse": mse / len(objPoints),
                        "rms": rms,
                        "objPoints": [obj.tolist() for obj in objPoints],
                        "imgPoints": [img.tolist() for img in imgPoints],
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

        except AttributeError:
            raise ValueError(f"Invalid ArUco dictionary name: {arucoDictName}")

    else:
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

        chessboardFound = [] # list of images with chessboard detected properly

        for fileName in images:
            img = cv.imread(fileName)
            grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners1 = cv.findChessboardCorners(
                grayImg, (chessBoardSize[0], chessBoardSize[1]), None
            )

            # If found, add object points, image points (after refining them)
            if ret:
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
                    "mse": mse / len(objPoints),
                    "rms": rms,
                    "objPoints": [obj.tolist() for obj in objPoints],
                    "imgPoints": [img.tolist() for img in imgPoints],
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

    cv.destroyAllWindows()

    if showListOfImagesWithChessboardFound:
        print("\nList of images with chessboard found:\n")
        print(chessboardFound)

