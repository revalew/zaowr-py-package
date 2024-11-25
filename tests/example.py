if __name__ == "__main__":
    from zaowr_polsl_kisiel import stereo_calibration, stereo_rectify, are_params_valid

    left_cam = r"/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam2/"
    right_cam = r"/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam3/"

    left_cam_params = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/calibration_params/calibration_params_left.json"
    right_cam_params = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/calibration_params/calibration_params_right.json"
    stereo_cam_params = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/calibration_params/stereo_calibration_params.json"

    rectified_images_dir = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/rectified_images"

    left_valid, params_left = are_params_valid(left_cam_params)
    right_valid, params_right = are_params_valid(right_cam_params)
    stereo_valid, stereo_params = are_params_valid(stereo_cam_params)

    if not left_valid or not right_valid or not stereo_valid:
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

        # Revalidate parameters after calibration
        left_valid, params_left = are_params_valid(left_cam_params)
        right_valid, params_right = are_params_valid(right_cam_params)
        stereo_valid, stereo_params = are_params_valid(stereo_cam_params)

        # Check again to ensure parameters are valid
        if not left_valid or not right_valid or not stereo_valid:
            raise RuntimeError("Calibration failed. Parameters are still invalid.")

    stereo_rectify(
        calibImgDirPath_left=left_cam,
        calibImgDirPath_right=right_cam,
        imgPoints_left=params_left["imgPoints"],
        imgPoints_right=params_right["imgPoints"],
        loadStereoCalibrationParams=True,
        stereoCalibrationParamsPath=stereo_cam_params,
        saveRectifiedImages=True,
        rectifiedImagesDirPath=rectified_images_dir,
        whichImage=0,
        drawEpipolarLinesParams=(20, 3, 2)
    )

    stereo_rectify(
        calibImgDirPath_left=left_cam,
        calibImgDirPath_right=right_cam,
        imgPoints_left=params_left["imgPoints"],
        imgPoints_right=params_right["imgPoints"],
        loadStereoCalibrationParams=True,
        stereoCalibrationParamsPath=stereo_cam_params,
        testInterpolationMethods=True,
        saveRectifiedImages=True,
        rectifiedImagesDirPath=rectified_images_dir,
        whichImage=0,
        drawEpipolarLinesParams=(20, 3, 2)
    )