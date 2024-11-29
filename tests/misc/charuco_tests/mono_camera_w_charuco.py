if __name__ == "__main__":
    # imgPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Charuco/Mono/s1/20231207_1320050.jpg"
    #
    # find_aruco_dict(imgPath)
    # exit(0)

    import zaowr_polsl_kisiel as zw

    charucoCalibration = True
    undistortImg = True

    if charucoCalibration:

        calibrationFile = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/calibration_params/calibration_params_charuco.json"

        imgPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Charuco/Mono/s1/"

        sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

        if not sub_valid:
            zw.calibrate_camera(
                chessBoardSize=(8, 11),
                squareRealDimensions=44.0,
                calibImgDirPath=imgPath,
                saveCalibrationParams=True,
                calibrationParamsPath=calibrationFile,
                displayFoundCorners=False,
                globImgExtension="jpg",
                useCharuco=True,
                charucoDictName="DICT_6X6_50",
                markerLength=34.0,
            )

            sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)
            if not sub_valid:
                raise RuntimeError("Calibration failed. Parameters are still invalid.")

    else:

        calibrationFile_normal = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/calibration_params/calibration_params.json"

        imgPath_normal = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/"

        sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile_normal)

        if not sub_valid:
            zw.calibrate_camera(
                chessBoardSize=(10, 7),
                squareRealDimensions=28.67,
                calibImgDirPath=imgPath_normal,
                saveCalibrationParams=True,
                calibrationParamsPath=calibrationFile_normal,
                displayFoundCorners=False,
            )

            sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile_normal)
            if not sub_valid:
                raise RuntimeError("Calibration failed. Parameters are still invalid.")

    imgToUndistort = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/Lab 1/Sprawko/src/img/distorted.png"


    if sub_valid:
        print("\nParameters are valid.")

    if undistortImg:
        # calibrationParams1 = zw.load_calibration(calibrationFile)
        cameraMatrix1 = calibrationParams1["cameraMatrix"]
        distortionCoef1 = calibrationParams1["distortionCoefficients"]

        zw.remove_distortion(
            cameraMatrix=cameraMatrix1,
            distortionCoefficients=distortionCoef1,
            imgToUndistortPath=imgToUndistort,
            showUndistortedImg=True,
        )