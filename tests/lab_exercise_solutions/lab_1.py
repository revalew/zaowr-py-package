if __name__ == "__main__":
    import zaowr_polsl_kisiel as zw

    calibrationFile = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/calibration_params/calibration_params.json"
    calibrationFileNoSubPix = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/calibration_params/calibration_params_no_subpix.json"

    imgPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/"

    imgToUndistort = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/Lab 1/Sprawko/src/img/distorted.png"

    sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)
    nosub_valid, calibrationParams2 = zw.are_params_valid(calibrationFileNoSubPix)

    if not sub_valid:
        zw.calibrate_camera(
            chessBoardSize=(10, 7),
            squareRealDimensions=28.67,
            calibImgDirPath=imgPath,
            saveCalibrationParams=True,
            calibrationParamsPath=calibrationFile,
            displayFoundCorners=False,
        )

        sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

        if not sub_valid:
            raise RuntimeError("Calibration failed. Parameters are still invalid.")

    if not nosub_valid:
        zw.calibrate_camera(
            chessBoardSize=(10, 7),
            squareRealDimensions=28.67,
            calibImgDirPath=imgPath,
            saveCalibrationParams=True,
            calibrationParamsPath=calibrationFileNoSubPix,
            displayFoundCorners=False,
            improveSubPix=False,
        )

        nosub_valid, calibrationParams2 = zw.are_params_valid(calibrationFileNoSubPix)

        if not sub_valid:
            raise RuntimeError("Calibration failed. Parameters are still invalid.")

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
