import cv2
import zaowr_polsl_kisiel as zw
import numpy as np

@zw.measure_perf()
def main():
    calibrationFile = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/calib.txt"

    calibrationParams = zw.load_depth_map_calibration( # this is the correct function
    # calibrationParams = zw.load_dept_map_calibration( # this one has a typo, but it works (will be fixed in 0.0.31)
        calibFile=calibrationFile
    )

    ##################################
    # EX 1
    ##################################
    disparityMapPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/disp0.pfm"

    ex_1_disparityMapPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_1_disparity.png"

    ex_1_depthMapPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_1_depth.png"

    disparityMap, scale = zw.load_pfm_file(
        filePath=disparityMapPath
    )

    depthMap = zw.disparity_to_depth_map(
        disparityMap=disparityMap,
        baseline=calibrationParams["baseline"],
        focalLength=calibrationParams["focalLength"],
        aspect=1000.0 # return depth in meters
    )

    depthMap_8bit = zw.depth_map_normalize(
        depthMap=depthMap,
        normalizeDepthMapRange="8-bit"
    )

    zw.display_img_plt(
        img=disparityMap,
        pltLabel="Disparity map",
        save=True,
        savePath=ex_1_disparityMapPath
    )

    zw.display_img_plt(
        img=depthMap_8bit,
        pltLabel="Depth map",
        save=True,
        savePath=ex_1_depthMapPath,
    )

    ##################################
    # EX 2
    ##################################
    img_left_path = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/im0.png"

    img_right_path = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/im1.png"

    ex_2_disparityMapPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_2_disparity.png"

    ex_2_depthMapPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_2_depth.png"

    ex_2_disparityMapComparisonPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_2_disparity_comparison.png"

    ex_2_depthMapComparisonPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_2_depth_comparison.png"

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
        aspect=1000.0
    )

    depthMapSGBM_8bit = zw.depth_map_normalize(
        depthMap=depthMapSGBM,
        normalizeDepthMapRange="8-bit"
    )

    zw.display_img_plt(
        img=disparityMapSGBM,
        pltLabel="Disparity map",
        save=True,
        savePath=ex_2_disparityMapPath
    )

    zw.display_img_plt(
        img=depthMapSGBM_8bit,
        pltLabel="Depth map",
        save=True,
        savePath=ex_2_depthMapPath,
    )

    zw.compare_images(
        images=[disparityMap, disparityMapSGBM],
        cmaps=["gray", "gray"],
        pltLabel="Disparity map comparison",
        titles=["Ground truth", "StereoSGBM"],
        nrows=1,
        ncols=2,
        save=True,
        savePath=ex_2_disparityMapComparisonPath
    )

    zw.compare_images(
        images=[depthMap_8bit, depthMapSGBM_8bit],
        cmaps=["gray", "gray"],
        pltLabel="Depth map comparison",
        titles=["Ground truth", "StereoSGBM"],
        nrows=1,
        ncols=2,
        save=True,
        savePath=ex_2_depthMapComparisonPath
    )

    ##################################
    # EX 3
    ##################################
    ex_3_depthMapRefPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_3_depth_ref.png"

    ex_3_depthMapSGBMPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_3_depth_sgbm.png"

    ex_3_depthMapComparisonPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_3_depth_comparison.png"

    depthMap_24bit = zw.depth_map_normalize(
        depthMap=depthMap,
        normalizeDepthMapRange="24-bit"
    )

    depthMapSGBM_24bit = zw.depth_map_normalize(
        depthMap=depthMapSGBM,
        normalizeDepthMapRange="24-bit"
    )

    zw.display_img_plt(
        img=depthMap_24bit,
        pltLabel="Depth map reference (24-bit)",
        save=True,
        savePath=ex_3_depthMapRefPath,
    )

    zw.display_img_plt(
        img=depthMapSGBM_24bit,
        pltLabel="Depth map StereoSGBM (24-bit)",
        save=True,
        savePath=ex_3_depthMapSGBMPath,
    )

    zw.compare_images(
        images=[depthMap_24bit, depthMapSGBM_24bit],
        cmaps=["gray", "gray"],
        pltLabel="Depth map comparison",
        titles=["Ground truth (24-bit)", "StereoSGBM (24-bit)"],
        nrows=1,
        ncols=2,
        save=True,
        savePath=ex_3_depthMapComparisonPath
    )

    ##################################
    # EX 4
    ##################################
    ex_4_disparityMapPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_4_disparity.png"

    ex_4_depthMapPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_4_depth.png"

    ex_4_comparisonPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_4_comparison.png"

    deptMapRef_24bit = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/depth.png"

    hFOV = 60
    imgWidth = 1920
    baseline = 0.1 # meters
    maxDepth = 1000.0 # meters
    depthMap_uint24 = cv2.imread(deptMapRef_24bit, cv2.IMREAD_UNCHANGED)
    focalLength = (depthMap_uint24.shape[0] / 2) / np.tan(np.radians(hFOV) / 2)
    # print(f"{type(focalLength) = }") # <class 'numpy.float64'>

    depthMap_ex4 = zw.decode_depth_map(
        depthMap=depthMap_uint24,
        maxDepth=maxDepth,
        decodeDepthMapRange="24-bit",
    )

    disparityMap_ex4 = zw.depth_to_disparity_map(
        depthMap=depthMap_ex4,
        baseline=baseline,
        focalLength=focalLength,
        minDepth=0.0,
    )

    cv2.imwrite(ex_4_disparityMapPath, disparityMap_ex4)
    # zw.display_img_plt(
    #     img=disparityMap_ex4,
    #     pltLabel="Disparity map",
    #     save=True,
    #     savePath=ex_4_disparityMapPath
    # )

    cv2.imwrite(ex_4_depthMapPath, depthMap_ex4)
    # zw.display_img_plt(
    #     img=depthMap_ex4,
    #     pltLabel="Depth map",
    #     save=True,
    #     savePath=ex_4_depthMapPath,
    # )

    zw.compare_images(
        images=[
            np.array(cv2.cvtColor(depthMap_uint24, cv2.COLOR_BGR2RGB)),
            depthMap_ex4,
            disparityMap_ex4,
        ],
        cmaps=[None, "gray", "gray"],
        pltLabel="Depth and disparity map comparison",
        titles=["Ground truth depth map (24-bit)", "Ground truth depth map Normalized", "Decoded disparity map"],
        nrows=1,
        ncols=3,
        save=True,
        savePath=ex_4_comparisonPath,
    )

    ##################################
    # EX 5
    ##################################
    imgPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/left.png"

    plyPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/depth_maps/results/ex_5.ply"

    img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
    disparityMap_ex5 = cv2.imread(ex_4_disparityMapPath, cv2.IMREAD_GRAYSCALE)
    depthMap_ex5 = cv2.imread(ex_4_depthMapPath, cv2.IMREAD_GRAYSCALE)

    h, w = depthMap_ex5.shape[:2]
    if img.shape[:2] != (h, w):
        img = cv2.resize(
            img,
            (w, h),
            interpolation=cv2.INTER_AREA
        )

    if disparityMap_ex5.shape[:2] != (h, w):
        disparityMap_ex5 = cv2.resize(
            disparityMap_ex5,
            (w, h),
            interpolation=cv2.INTER_AREA
        )

    f = 0.8 * w # focal length
    Q = np.float32([[1, 0, 0, -0.5 * w],
                    [0, -1, 0, 0.5 * h], # turn points 180 deg around x-axis,
                    [0, 0, 0, -f], # so that y-axis looks up
                    [0, 0, 1, 0]])

    points = cv2.reprojectImageTo3D(disparityMap_ex5, Q)
    colors = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mask = depthMap_ex5 < 50

    outPoints = points[mask]
    outColors = colors[mask]

    zw.write_ply_file(
        fileName=plyPath,
        verts=outPoints,
        colors=outColors,
    )


if __name__ == '__main__':
    main()