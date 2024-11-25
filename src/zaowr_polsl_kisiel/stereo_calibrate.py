from typing import Any
import numpy as np
import cv2 as cv
import glob
from .exceptions import CalibrationImagesNotFound, CalibrationParamsPathNotProvided, CalibrationParamsWrongFormat, StereoCalibrationParamsPathNotProvided

def calculate_fov(cameraMatrix: np.ndarray, imageSize: tuple[float, float]):
    """
    Calculate the horizontal and vertical FOV for a given camera.

    :param np.ndarray cameraMatrix: Intrinsic camera matrix (3x3).
    :param tuple[float, float] imageSize: Tuple containing image width and height (width, height).

    :return: tuple[float, float] Horizontal FOV and vertical FOV in degrees.
    """
    fx = cameraMatrix[0, 0]  # Focal length in x-axis
    fy = cameraMatrix[1, 1]  # Focal length in y-axis
    width, height = imageSize

    fov_horizontal = 2 * np.arctan(width / (2 * fx)) * (180 / np.pi)  # Convert radians to degrees
    fov_vertical = 2 * np.arctan(height / (2 * fy)) * (180 / np.pi)  # Convert radians to degrees

    return fov_horizontal, fov_vertical

def stereo_calibration(
    chessBoardSize: tuple[int, int],
    squareRealDimensions: float,
    calibImgDirPath_left: str,
    calibImgDirPath_right: str,
    globImgExtension: str = "png",
    saveCalibrationParams: bool = False,
    loadCalibrationParams: bool = False,
    calibrationParamsPath_left: str = "",
    calibrationParamsPath_right: str = "",
    saveStereoCalibrationParams: bool = False,
    stereoCalibrationParamsPath: str = "",
    displayFoundCorners: bool = False,
    displayMSE: bool = False,
    improveSubPix: bool = True,
    showListOfImagesWithChessboardFound: bool = False,
    terminationCriteria: tuple[Any, int, float] = (
        cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER,
        30,
        0.001,
    ),
    stereoCalibrationFlags: Any = cv.CALIB_FIX_INTRINSIC,
) -> None:
    """
    Perform stereo camera calibration using chessboard images from both left and right cameras. It also computes the Field of View (FOV) for both cameras, which is saved as part of the stereo calibration parameters.

    :param chessBoardSize: Tuple of integers representing the number of internal corners in the chessboard pattern (rows, columns).
    :param squareRealDimensions: Real-world size of each square on the chessboard in millimeters.
    :param calibImgDirPath_left: Path to the directory containing calibration images for the left camera.
    :param calibImgDirPath_right: Path to the directory containing calibration images for the right camera.
    :param globImgExtension: Extension of the calibration images (default is "png").
    :param saveCalibrationParams: Whether to save the individual camera calibration parameters (default is False).
    :param loadCalibrationParams: Whether to load pre-calibrated parameters for the cameras (default is False).
    :param calibrationParamsPath_left: Path to the pre-calibrated parameters for the left camera (default is empty).
    :param calibrationParamsPath_right: Path to the pre-calibrated parameters for the right camera (default is empty).
    :param saveStereoCalibrationParams: Whether to save the stereo calibration parameters (default is False).
    :param stereoCalibrationParamsPath: Path to save the stereo calibration parameters (default is empty).
    :param displayFoundCorners: Whether to display the found chessboard corners during calibration (default is False).
    :param displayMSE: Whether to display the Mean Squared Error (MSE) during calibration (default is False).
    :param improveSubPix: Whether to refine the corner detection to sub-pixel accuracy (default is True).
    :param showListOfImagesWithChessboardFound: Whether to display the list of images where the chessboard was detected (default is False).
    :param terminationCriteria: Criteria for corner refinement, in the form of a tuple (type, max_iter, epsilon) (default is set to terminate after 30 iterations or when epsilon is less than 0.001).
    :param stereoCalibrationFlags: Flags for stereo calibration (default is to fix intrinsic parameters using cv.CALIB_FIX_INTRINSIC).

    :return: None

    :raises CalibrationImagesNotFound: If calibration images for the left or right camera are not found in the specified directories.
    :raises CalibrationParamsPathNotProvided: If the path to save or load calibration parameters is not provided when required.
    :raises CalibrationParamsWrongFormat: If the calibration parameters are not in the correct format.
    :raises StereoCalibrationParamsPathNotProvided: If the path to save stereo calibration parameters is not provided when required.
    """
    if not loadCalibrationParams:
        ######################################################################################
        # Calibrate both cameras
        ######################################################################################
        objP = np.zeros((chessBoardSize[0] * chessBoardSize[1], 3), np.float32)
        objP[:, :2] = (
            np.mgrid[0 : chessBoardSize[0], 0 : chessBoardSize[1]].T.reshape(-1, 2)
            * squareRealDimensions
        )

        # Arrays to store object points and image points from all the images.
        objPoints = []  # 3d point in real world space
        imgPoints_left = []  # 2d points in image plane.
        imgPoints_right = []  # 2d points in image plane.

        # e.g. "../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/*.png"
        images_left = glob.glob(calibImgDirPath_left + "/*." + globImgExtension)
        images_right = glob.glob(calibImgDirPath_right + "/*." + globImgExtension)

        chessboardFound = {} # list of images with chessboard detected properly

        if (not images_left) or (len(images_left) == 0):
            raise CalibrationImagesNotFound

        if (not images_right) or (len(images_right) == 0):
            raise CalibrationImagesNotFound

        for i, _ in enumerate(images_left):
            img_left = cv.imread(images_left[i])
            grayImg_left = cv.cvtColor(img_left, cv.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret_left, corners_left = cv.findChessboardCorners(
                grayImg_left, (chessBoardSize[0], chessBoardSize[1]), None
            )

            # If found, add object points, image points (after refining them)
            if ret_left:
                img_right = cv.imread(images_right[i])
                grayImg_right = cv.cvtColor(img_right, cv.COLOR_BGR2GRAY)
                ret_right, corners_right = cv.findChessboardCorners(
                    grayImg_right, (chessBoardSize[0], chessBoardSize[1]), None
                )

                if not ret_right:
                    continue

                # chessboardFound[i] = f"L: {images_left[i]},  R: {images_right[i]}"
                chessboardFound[f"{i}_L"] = images_left[i]
                chessboardFound[f"{i}_R"] = images_right[i]

                objPoints.append(objP)

                if improveSubPix:
                    # LEFT
                    corners_left_improved = cv.cornerSubPix(
                        grayImg_left, corners_left, (11, 11), (-1, -1), terminationCriteria
                    )
                    imgPoints_left.append(corners_left_improved)

                    # RIGHT
                    corners_right_improved = cv.cornerSubPix(
                        grayImg_right, corners_right, (11, 11), (-1, -1), terminationCriteria
                    )
                    imgPoints_right.append(corners_right_improved)

                    if displayFoundCorners:
                        # Draw and display the corners
                        # LEFT
                        cv.drawChessboardCorners(
                            img_left, (chessBoardSize[0], chessBoardSize[1]), corners_left_improved, ret_left
                        )
                        cv.imshow("Current Image", img_left)
                        cv.waitKey(500)

                        # RIGHT
                        cv.drawChessboardCorners(
                            img_right, (chessBoardSize[0], chessBoardSize[1]), corners_right_improved, ret_right
                        )
                        cv.imshow("Current Image", img_right)
                        cv.waitKey(500)

                else:
                    imgPoints_left.append(corners_left)
                    imgPoints_right.append(corners_right)

                    if displayFoundCorners:
                        # Draw and display the corners
                        # LEFT
                        cv.drawChessboardCorners(
                            img_left, (chessBoardSize[0], chessBoardSize[1]), corners_left, ret_left
                        )
                        cv.imshow("Current Image", img_left)
                        cv.waitKey(500)

                        # RIGHT
                        cv.drawChessboardCorners(
                            img_right, (chessBoardSize[0], chessBoardSize[1]), corners_right, ret_right
                        )
                        cv.imshow("Current Image", img_right)
                        cv.waitKey(500)

        cv.destroyAllWindows()

        if showListOfImagesWithChessboardFound:
            print("\nList of images with chessboard found:\n")
            print(chessboardFound)

        # overall RMS re-projection error, camera matrix, distortion coefficients, rotation vectors, translation vectors
        rms_left, cameraMatrix_left, distortionCoefficients_left, rotationVectors_left, translationVectors_left = (
            cv.calibrateCamera(objPoints, imgPoints_left, grayImg_left.shape[::-1], None, None)
        )

        rms_right, cameraMatrix_right, distortionCoefficients_right, rotationVectors_right, translationVectors_right = (
            cv.calibrateCamera(objPoints, imgPoints_right, grayImg_right.shape[::-1], None, None)
        )

        mse_left = 0
        mse_right = 0
        for i in range(len(objPoints)):
            imgPoints_left_improved, _ = cv.projectPoints(
                objPoints[i],
                rotationVectors_left[i],
                translationVectors_left[i],
                cameraMatrix_left,
                distortionCoefficients_left,
            )
            error = cv.norm(imgPoints_left[i], imgPoints_left_improved, cv.NORM_L2) / len(imgPoints_left_improved)
            mse_left += error

            imgPoints_right_improved, _ = cv.projectPoints(
                objPoints[i],
                rotationVectors_right[i],
                translationVectors_right[i],
                cameraMatrix_right,
                distortionCoefficients_right,
            )
            error = cv.norm(imgPoints_right[i], imgPoints_right_improved, cv.NORM_L2) / len(imgPoints_right_improved)
            mse_right += error

        if displayMSE:
            print(f"\nmse_left: {mse_left / len(objPoints)}")
            print(f"\nmse_right: {mse_right / len(objPoints)}")

        if saveCalibrationParams:
            try:
                from .save_calibration import save_calibration

                calibrationParams_left = {
                    "mse": mse_left,
                    "rms": rms_left,
                    "objPoints": [obj.tolist() for obj in objPoints],
                    "imgPoints": [img.tolist() for img in imgPoints_left],
                    "cameraMatrix": cameraMatrix_left.tolist(),
                    "distortionCoefficients": distortionCoefficients_left.tolist(),
                    "rotationVectors": [rvec.tolist() for rvec in rotationVectors_left],
                    "translationVectors": [tvec.tolist() for tvec in translationVectors_left],
                }

                save_calibration(calibrationParams_left, calibrationParamsPath_left)

                calibrationParams_right = {
                    "mse": mse_right,
                    "rms": rms_right,
                    "objPoints": [obj.tolist() for obj in objPoints],
                    "imgPoints": [img.tolist() for img in imgPoints_right],
                    "cameraMatrix": cameraMatrix_right.tolist(),
                    "distortionCoefficients": distortionCoefficients_right.tolist(),
                    "rotationVectors": [rvec.tolist() for rvec in rotationVectors_right],
                    "translationVectors": [tvec.tolist() for tvec in translationVectors_right],
                }

                save_calibration(calibrationParams_right, calibrationParamsPath_right)

            except CalibrationParamsPathNotProvided:
                print("\nError occurred while saving the calibration parameters!\n")
                raise

            except Exception as e:
                print("\nUnknown error occurred\n")
                raise

    else:
        try:
            from .load_calibration import load_calibration

            calibrationParams_left = load_calibration(calibrationParamsPath_left)

            # mse_left = calibrationParams_left["mse"]
            # rms_left = calibrationParams_left["rms"]
            objPoints = calibrationParams_left["objPoints"]
            imgPoints_left = calibrationParams_left["imgPoints"]
            cameraMatrix_left = calibrationParams_left["cameraMatrix"]
            distortionCoefficients_left = calibrationParams_left["distortionCoefficients"]
            rotationVectors_left = calibrationParams_left["rotationVectors"]
            translationVectors_left = calibrationParams_left["translationVectors"]

            calibrationParams_right = load_calibration(calibrationParamsPath_right)

            # mse_right = calibrationParams_right["mse"]
            # rms_right = calibrationParams_right["rms"]
            imgPoints_right = calibrationParams_right["imgPoints"]
            cameraMatrix_right = calibrationParams_right["cameraMatrix"]
            distortionCoefficients_right = calibrationParams_right["distortionCoefficients"]
            rotationVectors_right = calibrationParams_right["rotationVectors"]
            translationVectors_right = calibrationParams_right["translationVectors"]

            images_left = glob.glob(calibImgDirPath_left + "/*." + globImgExtension)
            images_right = glob.glob(calibImgDirPath_right + "/*." + globImgExtension)

            if (not images_left) or (len(images_left) == 0):
                raise CalibrationImagesNotFound

            if (not images_right) or (len(images_right) == 0):
                raise CalibrationImagesNotFound

        except CalibrationParamsPathNotProvided:
            print("\nError occurred while loading the calibration parameters!\n")
            raise

        except CalibrationParamsWrongFormat:
            print("\nCalibration parameters are not in the correct format!\n")
            raise

        except Exception as e:
            print("\nUnknown error occurred\n")
            raise


    ######################################################################################
    # Stereo calibration
    ######################################################################################
    image_size = grayImg_left.shape[::-1]  # (width, height)

    ret, CM1, dist1, CM2, dist2, R, T, E, F = cv.stereoCalibrate(
        objPoints,  # Object points
        imgPoints_left,  # Image points from the left camera
        imgPoints_right,  # Image points from the right camera
        cameraMatrix_left,  # Camera matrix for the left camera
        distortionCoefficients_left,  # Distortion coefficients for the left camera
        cameraMatrix_right,  # Camera matrix for the right camera
        distortionCoefficients_right,  # Distortion coefficients for the right camera
        image_size,  # Image size (assumes both cameras have the same resolution)
        criteria=terminationCriteria,  # Termination criteria
        flags=stereoCalibrationFlags  # Stereo calibration flags
    )

    baseline = np.round((np.linalg.norm(T)) * 0.1, 2) # baseline in cm

    # Field of View for the Left and Right Cameras
    # Calculate FOV using cameraMatrix_left and cameraMatrix_right from single camera calibration
    fov_left = calculate_fov(cameraMatrix_left, image_size)
    fov_right = calculate_fov(cameraMatrix_right, image_size)

    if saveStereoCalibrationParams:
        try:
            from .save_calibration import save_calibration

            stereoCalibrationParams = {
                "reprojectionError": ret,
                "fov_left": list(fov_left),  # FOV as list (converted to tuple on load)
                "fov_right": list(fov_right),  # FOV as list (converted to tuple on load)
                "baseline": baseline,
                "cameraMatrix_left": CM1.tolist(),
                "distortionCoefficients_left": dist1.tolist(),
                "cameraMatrix_right": CM2.tolist(),
                "distortionCoefficients_right": dist2.tolist(),
                "rotationMatrix": R.tolist(),
                "translationVector": T.tolist(),
                "essentialMatrix": E.tolist(),
                "fundamentalMatrix": F.tolist(),
            }

            save_calibration(stereoCalibrationParams, stereoCalibrationParamsPath)

        except StereoCalibrationParamsPathNotProvided:
            print("\nError occurred while saving the stereo calibration parameters!\n")
            raise

        except Exception as e:
            print("\nUnknown error occurred\n")
            raise


# if __name__ == "__main__":
#     stereo_calibration(
#         chessBoardSize = (10, 7),
#         squareRealDimensions = 28.67,
#         calibImgDirPath_left = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam2/",
#         calibImgDirPath_right = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam3/",
#         globImgExtension = "png"
#     )