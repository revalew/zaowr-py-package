"""
KOLOKWIUM 2024
ZAOWR
IGT
MAKSYMILIAN KISIEL

LINK DO REPOZYTORIUM: https://github.com/revalew/zaowr-py-package
"""

if __name__ == "__main__":
    import glob
    from zaowr_polsl_kisiel import stereo_calibration, stereo_rectify, are_params_valid, save_calibration, remove_distortion, calibrate_camera

    # IMG DIR
    left_cam = r"/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/kolokwium-zestaw/left/"
    right_cam = r"/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/kolokwium-zestaw/right/"

    # MONO CAM PARAMS
    left_cam_params_mono = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/json/zadanie_1_1_calibration_params_mono_left.json"
    right_cam_params_mono = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/json/zadanie_1_1_calibration_params_mono_right.json"

    # IMG TO UNDISTORT (MONO CAM)
    imgToUndistort_left = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/kolokwium-zestaw/left/1.png"
    imgToUndistort_right = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/kolokwium-zestaw/right/1.png"

    # UNDISTORTED IMG
    undistorted_left = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/undistorted/1_undistorted_left.png"
    undistorted_right = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/undistorted/1_undistorted_right.png"

    # STEREO CAM PARAMS FOR EACH CAMERA
    left_cam_params_stereo = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/json/calibration_params_stereo_left.json"
    right_cam_params_stereo = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/json/calibration_params_stereo_right.json"

    # STEREO CAM PARAMS AFTER STEREO CALIBRATION
    stereo_cam_params = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/json/stereo_calibration_params.json"

    # SAVE IMG AFTER RECTIFICATION
    rectified_images_dir = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/rectified_images"

    #############################################################
    # ZADANIE 1.1 i 1.3 jako `showListOfImagesWithChessboardFound=True`
    #############################################################
    # Wyznacz oraz zapisz wartości macierzy parametrów wewnętrznych dla lewej i prawej kamery.Krótko opisz co reprezentują wyznaczone wartości.
    # MONO LEFT
    print("\n\n\nMONO LEFT\n\n\n")
    sub_valid, calibrationParams1 = are_params_valid(left_cam_params_mono)

    if not sub_valid:
        calibrate_camera(
            chessBoardSize=(10, 7),
            squareRealDimensions=50.0,
            calibImgDirPath=left_cam,
            saveCalibrationParams=True,
            calibrationParamsPath=left_cam_params_mono,
            displayFoundCorners=False,
            showListOfImagesWithChessboardFound=True
        )

        sub_valid, calibrationParams1 = are_params_valid(left_cam_params_mono)

        if not sub_valid:
            raise RuntimeError("Calibration failed. Parameters are still invalid.")

    # MONO RIGHT
    print("\n\n\nMONO RIGHT\n\n\n")
    sub_valid, calibrationParams2 = are_params_valid(right_cam_params_mono)

    if not sub_valid:
        calibrate_camera(
            chessBoardSize=(10, 7),
            squareRealDimensions=50.0,
            calibImgDirPath=right_cam,
            saveCalibrationParams=True,
            calibrationParamsPath=right_cam_params_mono,
            displayFoundCorners=False,
            showListOfImagesWithChessboardFound=True
        )

        sub_valid, calibrationParams2 = are_params_valid(right_cam_params_mono)

        if not sub_valid:
            raise RuntimeError("Calibration failed. Parameters are still invalid.")

    #############################################################
    # ZADANIE 1.2
    #############################################################
    # Wyznacz oraz zapisz współczynniki dystorsji [k1, k2, k3, p1, p2] dla lewej i prawej kamery
    zadanie_1_2_left = {
        "k1": calibrationParams1["distortionCoefficients"][0][0],
        "k2": calibrationParams1["distortionCoefficients"][0][1],
        "p1": calibrationParams1["distortionCoefficients"][0][2],
        "p2": calibrationParams1["distortionCoefficients"][0][3],
        "k3": calibrationParams1["distortionCoefficients"][0][4],
    }

    zadanie_1_2_right = {
        "k1": calibrationParams2["distortionCoefficients"][0][0],
        "k2": calibrationParams2["distortionCoefficients"][0][1],
        "p1": calibrationParams2["distortionCoefficients"][0][2],
        "p2": calibrationParams2["distortionCoefficients"][0][3],
        "k3": calibrationParams2["distortionCoefficients"][0][4],
    }

    save_calibration(zadanie_1_2_left, "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/json/zadanie_1_2_left.json")
    save_calibration(zadanie_1_2_right, "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2024/json/zadanie_1_2_right.json")


    #############################################################
    # ZADANIE 1.4
    #############################################################
    # Usuń dystorsję dla wybranej klatki z lewej oraz prawej kamery. W rozwiązaniu zamieść nazwy plików które zostały użyte oraz wyniki operacji w formie zdjęcia.
    remove_distortion(
        cameraMatrix=calibrationParams1["cameraMatrix"],
        distortionCoefficients=calibrationParams1["distortionCoefficients"],
        imgToUndistortPath=imgToUndistort_left,
        showUndistortedImg=False,
        saveUndistortedImg=True,
        undistortedImgPath=undistorted_right,
    )

    remove_distortion(
        cameraMatrix=calibrationParams2["cameraMatrix"],
        distortionCoefficients=calibrationParams2["distortionCoefficients"],
        imgToUndistortPath=imgToUndistort_right,
        showUndistortedImg=False,
        saveUndistortedImg=True,
        undistortedImgPath=undistorted_left,

    )

    #############################################################
    # ZADANIE 2.1, 2.2 z flagą `showListOfImagesWithChessboardFound=True`
    #############################################################
    # Wykonaj kalibrację systemu kamer stereo.(Brak pliku.json)
    left_valid, params_left = are_params_valid(left_cam_params_stereo)
    right_valid, params_right = are_params_valid(right_cam_params_stereo)
    stereo_valid, stereo_params = are_params_valid(stereo_cam_params)

    if not left_valid or not right_valid or not stereo_valid:
        # hover over function parameters to see what they do (if names are not enough...)
        stereo_calibration(
            chessBoardSize=(10, 7),
            # squareRealDimensions=28.67,
            squareRealDimensions=50.0,
            calibImgDirPath_left=left_cam,
            calibImgDirPath_right=right_cam,
            globImgExtension="png",
            saveCalibrationParams=True,
            calibrationParamsPath_left=left_cam_params_stereo,
            calibrationParamsPath_right=right_cam_params_stereo,
            saveStereoCalibrationParams=True,
            stereoCalibrationParamsPath=stereo_cam_params,
            showListOfImagesWithChessboardFound=True, # Zapisz listę plików użytych do kalibracji lewej i prawej kamery.
        )

        # Revalidate parameters after calibration
        left_valid, params_left = are_params_valid(left_cam_params_stereo)
        right_valid, params_right = are_params_valid(right_cam_params_stereo)
        stereo_valid, stereo_params = are_params_valid(stereo_cam_params)

        # Check again to ensure parameters are valid
        if not left_valid or not right_valid or not stereo_valid:
            raise RuntimeError("Calibration failed. Parameters are still invalid.")

    #############################################################
    # ZADANIE 2.3
    #############################################################
    # Zrektyfikuj wybraną parę obrazów. W rozwiązaniu zamieść nazwy plików które zostały użyte oraz wyniki operacji w formie zdjęcia.
    globImgExtension = "png"
    images_left = glob.glob(left_cam + "/*." + globImgExtension)
    images_right = glob.glob(right_cam + "/*." + globImgExtension)

    whichImage = 0

    img_to_rectify = {
        "left": images_left[whichImage],
        "right": images_right[whichImage]
    }

    print("\n\nPliki użyte do rektyfikacji")
    print(img_to_rectify)


    # hover over function parameters to see what they do (if names are not enough...)
    stereo_rectify(
        calibImgDirPath_left=left_cam,
        calibImgDirPath_right=right_cam,
        imgPoints_left=params_left["imgPoints"],
        imgPoints_right=params_right["imgPoints"],
        loadStereoCalibrationParams=True,
        stereoCalibrationParamsPath=stereo_cam_params,
        saveRectifiedImages=True,
        rectifiedImagesDirPath=rectified_images_dir,
        whichImage=whichImage,
        drawEpipolarLinesParams=(20, 3, 2)
    )

    #############################################################
    # ZADANIE 2.4
    #############################################################
    # Oblicz odległość pomiędzy kamerami (Baseline).
    baseline = stereo_params["baseline"]

    print(f"\n\nBaseline:\n\t{baseline} cmn\n\t{baseline / 100} m")

    #############################################################
    # ZADANIE 3
    #############################################################
    # Wyznacz HFov (Horizontal field of view) dla obu kamer.
    hFOV_left = stereo_params["fov_left"]
    hFOV_right = stereo_params["fov_right"]

    print(f"\n\nHorizontal field of view:\n\tLeft: {hFOV_left} degrees\n\tRight: {hFOV_right} degrees")