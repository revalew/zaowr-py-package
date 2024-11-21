from typing import Any
import numpy as np
import cv2 as cv
import glob


def calibrate_camera() -> None:
    dir_left = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam2/"
    dir_right = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam3/"
    chessBoardSize = (10, 7)
    squareRealDimensions = 28.67
    globImgExtension = "png"
    terminationCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

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
    images_left = glob.glob(dir_left + "/*." + globImgExtension)
    images_right = glob.glob(dir_right + "/*." + globImgExtension)

    # if (images_left == []) or (len(images_left) == 0):
    #     raise CalibrationImagesNotFound

    for i, _ in enumerate(images_left):

        # if i >= 8:
        #     break


        grayImg_left = cv.cvtColor(cv.imread(images_left[i]), cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret_left, corners_left = cv.findChessboardCorners(
            grayImg_left, (chessBoardSize[0], chessBoardSize[1]), None
        )

        # If found, add object points, image points (after refining them)
        if ret_left:
            grayImg_right = cv.cvtColor(cv.imread(images_right[i]), cv.COLOR_BGR2GRAY)
            ret_right, corners_right = cv.findChessboardCorners(
                grayImg_right, (chessBoardSize[0], chessBoardSize[1]), None
            )

            if not ret_right:
                continue

            objPoints.append(objP)

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


    cv.destroyAllWindows()

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


    print(f"\n{rms_left = }")
    print(f"\n{rms_right = }")

    print(f"\nmse_left: {mse_left / len(objPoints)}")
    print(f"\nmse_right: {mse_right / len(objPoints)}")

    # Stereo calibration
    stereocalibration_flags = cv.CALIB_FIX_INTRINSIC
    ret, CM1, dist1, CM2, dist2, R, T, E, F = cv.stereoCalibrate(
        objPoints,  # Object points
        imgPoints_left,  # Image points from the left camera
        imgPoints_right,  # Image points from the right camera
        cameraMatrix_left,  # Camera matrix for the left camera
        distortionCoefficients_left,  # Distortion coefficients for the left camera
        cameraMatrix_right,  # Camera matrix for the right camera
        distortionCoefficients_right,  # Distortion coefficients for the right camera
        grayImg_left.shape[::-1],  # Image size (assumes both cameras have the same resolution)
        criteria=terminationCriteria,  # Termination criteria
        flags=stereocalibration_flags  # Stereo calibration flags
    )

    baseline = np.round((np.linalg.norm(T)) * 0.1, 2) # baseline in cm
    print(f"{baseline = } cm")

    print(f"\nStereo Calibration RMS error: {ret}")
    print(f"\nRotation matrix R:\n{R}")
    print(f"\nTranslation vector T:\n{T}")
    print(f"\nEssential matrix E:\n{E}")
    print(f"\nFundamental matrix F:\n{F}")

    # Stereo Rectification
    R1, R2, P1, P2, Q, roi1, roi2 = cv.stereoRectify(
        cameraMatrix_left, distortionCoefficients_left, cameraMatrix_right, distortionCoefficients_right,
        grayImg_left.shape[::-1], R, T
    )

    # Create rectification maps
    map1_left, map2_left = cv.initUndistortRectifyMap(cameraMatrix_left, distortionCoefficients_left, R1, P1,
                                                      grayImg_left.shape[::-1], cv.CV_16SC2)
    map1_right, map2_right = cv.initUndistortRectifyMap(cameraMatrix_right, distortionCoefficients_right, R2, P2,
                                                        grayImg_left.shape[::-1], cv.CV_16SC2)

    # Load an example pair of images for rectification
    img_left = cv.imread(images_left[0])
    img_right = cv.imread(images_right[0])

    # Apply rectification to both images
    rectified_left = cv.remap(img_left, map1_left, map2_left, cv.INTER_LINEAR)
    rectified_right = cv.remap(img_right, map1_right, map2_right, cv.INTER_LINEAR)

    # Display the rectified images side by side
    rectified_pair = np.hstack((rectified_left, rectified_right))
    # Save the rectified image to a file

    cv.imwrite('rectified_left.png', rectified_left)
    cv.imwrite('rectified_right.png', rectified_right)
    cv.imwrite('rectified_stereo_pair.png', rectified_pair)

    cv.imshow('Rectified Stereo Images', rectified_pair)
    cv.waitKey(0)
    cv.destroyAllWindows()








    # if saveCalibrationParams:
    #     try:
    #         from .save_calibration import save_calibration

    # calibrationParams = {
    #     "mse_left": mse_left,
    #     "mse_right": mse_right,
    #     "imgPoints2": imgPoints2,
    #     "rms": rms,
    #     "cameraMatrix": cameraMatrix.tolist(),
    #     "distortionCoefficients": distortionCoefficients.tolist(),
    #     "rotationVectors": [rvec.tolist() for rvec in rotationVectors],
    #     "translationVectors": [tvec.tolist() for tvec in translationVectors],
    # }

        #     save_calibration(calibrationParams, calibrationParamsPath)
        #
        # except CalibrationParamsPathNotProvided:
        #     print("\nError occurred while saving the calibration parameters!\n")
        #     raise
        #
        # except Exception as e:
        #     print("\nUnknown error occurred\n")
        #     raise


if __name__ == "__main__":
    calibrate_camera()