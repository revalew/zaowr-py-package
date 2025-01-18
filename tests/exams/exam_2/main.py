"""
KOLOKWIUM 2, 2025
ZAOWR
IGT
MAKSYMILIAN KISIEL

LINK DO REPOZYTORIUM: https://github.com/revalew/zaowr-py-package
"""

import zaowr_polsl_kisiel as zw
import cv2
import numpy as np


# Get points form photo
def click_event(event, x, y, flags, param):
    image, points = param  # Rozpakowanie przekazanych parametrów
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Kliknięto w punkt: ({x}, {y})")
        points.append((x, y))
        # Rysowanie punktu na obrazie
        cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow("Obraz", image)

def get_points(img_path):
    points = []

    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    cv2.namedWindow("Obraz", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Obraz",(1080,720))
    cv2.imshow("Obraz", img)
    cv2.setMouseCallback("Obraz", click_event, (img, points))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return points

def get_depth_value_for_points(points, array, unit="m"):
    results = []
    for idx, (x, y) in enumerate(points, start=1):
        value = array[y, x]
        results.append((f"P{idx}", x, y, value))
        print(f"P{idx} ({x}, {y}): {value:.2f} {unit}")

    return results

def get_disparity_value_for_points(points, array, unit="px"):
    results = []
    for idx, (x, y) in enumerate(points, start=1):
        value = array[y, x]
        results.append((f"P{idx}", x, y, value))
        print(f"P{idx} ({x}, {y}): {value:.2f} {unit}")

    return results

def main():
    #############################################################
    # ZADANIE 1
    #############################################################
    # Odczytaj wartości z referencyjnej mapy głębi wygenerowanej przy użyciu symulatora CARLA (depth.png).

    # Odczyt
    deptMapRef_24bit = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/K2T1/K2T1/Z1Z2Z3/depth.png"

    depthMap_uint24 = cv2.imread(deptMapRef_24bit, cv2.IMREAD_UNCHANGED)

    # Konwersja na 8 bit
    maxDepth = 1000.0  # meters

    depthMap = zw.decode_depth_map(
        depthMap=depthMap_uint24,
        maxDepth=maxDepth,
        decodeDepthMapRange="24-bit",
    )

    # Odczytanie punktów ze zdjęcia i wyznaczenie odległości od kamery
    inputFolder = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/K2T1/K2T1/"

    inputInfoPath = inputFolder + "Z1Z2Z3/info.png"

    # Available in zaowr_polsl_kisiel package version 0.0.32
    # or higher (added because of the exam)
    # points = zw.get_image_points(imgPath=inputInfoPath)
    # results = zw.get_map_value_for_points(
    #       imgPoints=points,
    #       mapPoints=depthMap,
    #       mapType="depth")

    points = [(804, 474), (1630, 273), (343, 171)]
    # points = get_points(inputInfoPath)
    # print(f"{points = }")

    results = get_depth_value_for_points(points, depthMap, unit="m")
    # print(f"{results = }")

    # Kliknięto w punkt: (804, 474)
    # Kliknięto w punkt: (1630, 273)
    # Kliknięto w punkt: (343, 171)
    # P1 (804, 474): 21.88 m
    # P2 (1630, 273): 8.00 m
    # P3 (343, 171): 56.01 m

    # Zapis
    depthMapPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/results/img/z1depth.png"

    mask = depthMap == 50
    depthMap[mask] = 250

    mask = depthMap > 50
    depthMap[mask] = 255

    cv2.imwrite(depthMapPath, depthMap)

    #############################################################
    # ZADANIE 2
    #############################################################
    # Wyznacz mapę rozbieżności (disparity map) na podstawie referencyjnej mapy głębi (depth map).

    # Konwersja zdekodowanej mapy
    hFOV = 90
    baseline = 0.1  # meters
    maxDepth = 1000.0  # meters
    minDepth = 0.0  # meters
    focalLength = (depthMap_uint24.shape[0] / 2) / np.tan(np.radians(hFOV) / 2)

    disparityMap = zw.depth_to_disparity_map(
        depthMap=depthMap,
        baseline=baseline,
        focalLength=focalLength,
        minDepth=minDepth,
    )

    # Odczyt rozbieżności
    results = get_disparity_value_for_points(points, disparityMap, unit="px")
    # P1(804, 474): 12.00 px
    # P2(1630, 273): 37.00 px
    # P3(343, 171): 0.00 px

    # Zapis
    disparityMapPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/results/img/z2disparity.png"

    cv2.imwrite(disparityMapPath, disparityMap)

    #############################################################
    # ZADANIE 3
    #############################################################
    # Przekonwertuj referencyjną mapę głębi depth.png z zadania 1 na kolorową chmurę punktów w formacie PLY.
    imgPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/K2T1/K2T1/Z1Z2Z3/left.png"

    plyPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/results/z3.ply"

    img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
    disparityMap_ex5 = cv2.imread(disparityMapPath, cv2.IMREAD_GRAYSCALE)
    depthMap_ex5 = cv2.imread(depthMapPath, cv2.IMREAD_GRAYSCALE)

    h, w = depthMap_ex5.shape[:2]
    if img.shape[:2] != (h, w):
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)

    if disparityMap_ex5.shape[:2] != (h, w):
        disparityMap_ex5 = cv2.resize(
            disparityMap_ex5, (w, h), interpolation=cv2.INTER_AREA
        )

    f = 0.8 * w  # focal length
    Q = np.float32(
        [
            [1, 0, 0, -0.5 * w],
            [0, -1, 0, 0.5 * h],  # turn points 180 deg around x-axis,
            [0, 0, 0, -f],  # so that y-axis looks up
            [0, 0, 1, 0],
        ]
    )

    points = cv2.reprojectImageTo3D(disparityMap_ex5, Q)
    colors = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mask = depthMap_ex5 < 50

    outPoints = points[mask]
    outColors = colors[mask]

    # Available in zaowr_polsl_kisiel package version 0.0.32
    # or higher (added because of the exam)
    # outPoints, outColors = zw.create_color_point_cloud(
    #     colorImgPath=imgPath,
    #     disparityMapPath=disparityMapPath,
    #     depthMapPath=depthMapPath,
    #     focalLengthFactor=0.8,
    #     maxDepth=50.0)

    zw.write_ply_file(
        fileName=plyPath,
        verts=outPoints,
        colors=outColors,
    )

    #############################################################
    # ZADANIE 4
    #############################################################
    # Korzystając z metody StereoSGBM udostępnionej przez bibliotekę OpenCV wyznacz mapę rozbieżności oraz mapę głębi.
    img_left_path = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/K2T1/K2T1/Z4Z5/im0.png"

    img_right_path = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/K2T1/K2T1/Z4Z5/im1.png"

    calibrationFile = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/K2T1/K2T1/Z4Z5/calib.txt"

    disparityMapRefPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/K2T1/K2T1/Z4Z5/disp0.pfm"


    depthComparisonPath1 = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/results/img/z4depth.png"

    disparityComparisonPath1 = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/results/img/z4disparity.png"

    depthComparisonPath2 = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/results/img/z4depth_comparison.png"

    disparityComparisonPath2 = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/results/img/z4disparity_comparison.png"

    # Wczytaj kalibrację
    calibrationParams = zw.load_depth_map_calibration(
        calibFile=calibrationFile
    )

    # Wczytaj referencyjną mapę PFM
    disparityMap, scale = zw.load_pfm_file(filePath=disparityMapRefPath)

    depthMap = zw.disparity_to_depth_map(
        disparityMap=disparityMap,
        baseline=calibrationParams["baseline"],
        focalLength=calibrationParams["focalLength"],
        doffs=calibrationParams["doffs"],
        aspect=1000.0,  # return depth in meters
    )

    depthMap_8bit = zw.depth_map_normalize(
        depthMap=depthMap, normalizeDepthMapRange="8-bit"
    )

    # Oblicz nową mapę dysparycji za pomocą StereoSGBM
    disparityMapSGBM = zw.calculate_disparity_map(
        leftImagePath=img_left_path,
        rightImagePath=img_right_path,
        blockSize=9,
        numDisparities=256,
        minDisparity=0,
        disparityCalculationMethod="sgbm",
        normalizeDisparityMap=False,
    )

    disparityMapSGBM = disparityMapSGBM.astype(np.float32) / 16.0

    depthMapSGBM = zw.disparity_to_depth_map(
        disparityMap=disparityMapSGBM,
        baseline=calibrationParams["baseline"],
        focalLength=calibrationParams["focalLength"],
        doffs=calibrationParams["doffs"],
        aspect=1000.0,
    )

    depthMapSGBM_8bit = zw.depth_map_normalize(
        depthMap=depthMapSGBM, normalizeDepthMapRange="8-bit"
    )

    points = [(1550, 900)]

    # Available in zaowr_polsl_kisiel package version 0.0.32
    # or higher (added because of the exam)
    #
    # depth_gt = zw.get_map_value_for_points(
    #       imgPoints=points,
    #       mapPoints=depthMap,
    #       mapType="depth")
    #
    # disparity_gt = zw.get_map_value_for_points(
    #       imgPoints=points,
    #       mapPoints=disparityMap,
    #       mapType="disparity")

    print(f"\n\nX, Y = [{points[0][0]}, {points[0][1]}]\n\nGT:")
    depth_gt = get_depth_value_for_points(points, depthMap, unit="m")
    disparity_gt = get_disparity_value_for_points(points, disparityMap, unit="px")

    print(f"\nSGBM:")
    depth = get_depth_value_for_points(points, depthMapSGBM, unit="m")
    disparity = get_disparity_value_for_points(points, disparityMapSGBM, unit="px")

    cv2.imwrite(disparityComparisonPath1, disparityMapSGBM)
    cv2.imwrite(depthComparisonPath1, depthMapSGBM_8bit)

    zw.compare_images(
        images=[disparityMap, disparityMapSGBM],
        cmaps=["gray", "gray"],
        pltLabel="Disparity map comparison",
        titles=["Ground truth", "StereoSGBM"],
        nrows=1,
        ncols=2,
        save=True,
        savePath=disparityComparisonPath2,
    )

    zw.compare_images(
        images=[depthMap_8bit, depthMapSGBM_8bit],
        cmaps=["gray", "gray"],
        pltLabel="Depth map comparison",
        titles=["Ground truth", "StereoSGBM"],
        nrows=1,
        ncols=2,
        save=True,
        savePath=depthComparisonPath2,
    )

    #############################################################
    # ZADANIE 5
    #############################################################
    # Korzystając z własnej implementacji metody bazującej na dopasowaniu bloków omówionej podczas wykładów wyznacz mapę rozbieżności oraz mapę głębi dla pary obrazów kanonicznego układu stereo.

    # ZDJĘCIA W SKALI 0.25
    img_left_path = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/K2T1/K2T1/Z4Z5/im0_4.png"

    img_right_path = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/K2T1/K2T1/Z4Z5/im1_4.png"


    depthComparisonPath1 = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/results/img/z5depth.png"

    disparityComparisonPath1 = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/results/img/z5disparity.png"

    depthComparisonPath2 = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/results/img/z5depth_comparison.png"

    disparityComparisonPath2 = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/KOLOS_2_2024/results/img/z5disparity_comparison.png"

    # Oblicz nową mapę dysparycji za pomocą własnej implementacji
    disparityMapCustom = zw.calculate_disparity_map(
        leftImagePath=img_left_path,
        rightImagePath=img_right_path,
        maxDisparity=64,
        windowSize=(5, 5),
        disparityCalculationMethod="custom",
        # normalizeDisparityMap=False,
    )

    depthMapCustom = zw.disparity_to_depth_map(
        disparityMap=disparityMapCustom,
        baseline=calibrationParams["baseline"],
        focalLength=calibrationParams["focalLength"],
        doffs=calibrationParams["doffs"],
        aspect=1000.0,
    )

    depthMapCustom_8bit = zw.depth_map_normalize(
        depthMap=depthMapCustom, normalizeDepthMapRange="8-bit"
    )

    points = [(1550, 900)]

    # Available in zaowr_polsl_kisiel package version 0.0.32
    # or higher (added because of the exam)
    #
    # depth_gt = zw.get_map_value_for_points(
    #       imgPoints=points,
    #       mapPoints=depthMap,
    #       mapType="depth")
    #
    # disparity_gt = zw.get_map_value_for_points(
    #       imgPoints=points,
    #       mapPoints=disparityMap,
    #       mapType="disparity")

    print(f"\n\nX, Y = [{points[0][0]}, {points[0][1]}]\n\nGT:")
    depth_gt = get_depth_value_for_points(points, depthMap, unit="m")
    disparity_gt = get_disparity_value_for_points(points, disparityMap, unit="px")

    points = [(int(1550 / 4), int(900 / 4))]
    print(f"\nCUSTOM:")
    depth = get_depth_value_for_points(points, depthMapCustom, unit="m")
    disparity = get_disparity_value_for_points(points, disparityMapCustom, unit="px")

    cv2.imwrite(disparityComparisonPath1, disparityMapCustom)
    cv2.imwrite(depthComparisonPath1, depthMapCustom_8bit)

    zw.compare_images(
        images=[disparityMap, disparityMapCustom],
        cmaps=["gray", "gray"],
        pltLabel="Disparity map comparison",
        titles=["Ground truth", "Custom"],
        nrows=1,
        ncols=2,
        save=True,
        savePath=disparityComparisonPath2,
    )

    zw.compare_images(
        images=[depthMap_8bit, depthMapCustom_8bit],
        cmaps=["gray", "gray"],
        pltLabel="Depth map comparison",
        titles=["Ground truth", "Custom"],
        nrows=1,
        ncols=2,
        save=True,
        savePath=depthComparisonPath2,
    )




if __name__ == '__main__':
    main()