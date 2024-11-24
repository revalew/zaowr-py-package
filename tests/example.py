if __name__ == "__main__":
    from zaowr_polsl_kisiel.stereo_calibrate import stereo_calibration
    from zaowr_polsl_kisiel.load_calibration import load_calibration
    from zaowr_polsl_kisiel.stereo_rectify import stereo_rectify

    left_cam = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam2/"
    right_cam = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Stereo 1/cam3/"

    left_cam_params = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/calibration_params_left.json"
    right_cam_params = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/calibration_params_right.json"
    stereo_cam_params = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/stereo_calibration_params.json"

    stereo_calibration(
        chessBoardSize=(10, 7),
        squareRealDimensions=28.67,
        calibImgDirPath_left=left_cam,
        calibImgDirPath_right=right_cam,
        globImgExtension="png",
        saveCalibrationParams=True,
        calibrationParamsPath_left=left_cam_params,
        calibrationParamsPath_right=right_cam_params,
        saveStereoCalibrationParams=True,
        stereoCalibrationParamsPath=stereo_cam_params,
    )

    params_left = load_calibration(left_cam_params)
    params_right = load_calibration(right_cam_params)

    stereo_rectify(
        calibImgDirPath_left=left_cam,
        calibImgDirPath_right=right_cam,
        imgPoints_left=params_left["imgPoints"],
        imgPoints_right=params_right["imgPoints"],
        loadStereoCalibrationParams=True,
        stereoCalibrationParamsPath=stereo_cam_params,
        saveRectifiedImages=True,
        rectifiedImagesDirPath="/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/rectified_images",
    )