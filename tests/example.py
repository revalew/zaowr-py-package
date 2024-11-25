import cv2
def find_aruco_dict(imgPath):
    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }
    print("[INFO] loading image...")
    image = cv2.imread(imgPath)
    # loop over the types of ArUco dictionaries
    for (arucoName, arucoDict) in ARUCO_DICT.items():
        # load the ArUCo dictionary, gr ab the ArUCo parameters, and attempt to detect the markers for the current dictionary
        arucoDict = cv2.aruco.getPredefinedDictionary(arucoDict)
        arucoParams = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
        (corners, ids, rejected) = detector.detectMarkers(image)
        # if at least one ArUco marker was detected display the ArUco name to our terminal
        if len(corners) > 0:
            print("[INFO] detected {} markers for '{}'".format(
                len(corners), arucoName))


if __name__ == "__main__":
    # imgPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Charuco/Mono/s1/20231207_1320050.jpg"
    #
    # find_aruco_dict(imgPath)
    # exit(0)

    import zaowr_polsl_kisiel as zw

    calibrationFile = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/calibration_params/calibration_params_charuco.json"

    imgPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Charuco/Mono/s1/"

    imgToUndistort = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/Lab 1/Sprawko/src/img/distorted.png"

    sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

    if not sub_valid:
        zw.calibrate_camera(
            chessBoardSize=(10, 7),
            squareRealDimensions=44.0,
            calibImgDirPath=imgPath,
            saveCalibrationParams=True,
            calibrationParamsPath=calibrationFile,
            displayFoundCorners=False,
            globImgExtension="jpg",
            useCharuco=True,
            arucoDictName="DICT_6X6_50",
            markerLength=34.0,
        )

        sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

        if not sub_valid:
            raise RuntimeError("Calibration failed. Parameters are still invalid.")

    if sub_valid:
        print("\nParameters are valid.")

    exit(0)

    # calibrationParams1 = zw.load_calibration(calibrationFile)
    cameraMatrix1 = calibrationParams1["cameraMatrix"]
    distortionCoef1 = calibrationParams1["distortionCoefficients"]

    # calibrationParams2 = zw.load_calibration(calibrationFileNoSubPix)
    cameraMatrix2 = calibrationParams2["cameraMatrix"]
    distortionCoef2 = calibrationParams2["distortionCoefficients"]

    zw.remove_distortion(
        cameraMatrix=cameraMatrix1,
        distortionCoefficients=distortionCoef1,
        imgToUndistortPath=imgToUndistort,
        showUndistortedImg=True,
    )

    zw.remove_distortion(
        cameraMatrix=cameraMatrix2,
        distortionCoefficients=distortionCoef2,
        imgToUndistortPath=imgToUndistort,
        showUndistortedImg=True,
    )