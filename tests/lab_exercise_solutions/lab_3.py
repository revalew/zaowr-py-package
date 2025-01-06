import cv2
import zaowr_polsl_kisiel as zw

from sys import stderr
import os
from colorama import Fore, Style, init as colorama_init  # , Back
from tqdm import tqdm  # progress bar

colorama_init(autoreset=True)

@zw.measure_perf()
def main() -> None:
    # Paths to the images
    img_left = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/disparity_maps/cones/im0.ppm"
    img_right = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/disparity_maps/cones/im1.ppm"

    img_left_real_life = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/rectified_images/rectified_left.png"
    img_right_real_life = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/rectified_images/rectified_right.png"

    groundTruthPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/disparity_maps/cones/disp2.pgm"

    showMaps = False
    saveDisparityMap = True
    saveDisparityMapPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/disparity_maps/"

    saveComparison = True
    saveComparisonPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/disparity_maps/comparison_ppm.png"
    saveComparisonPath_RL = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/disparity_maps/comparison_rl.png"

    tasks = [
        "Calculating disparity map using BM (PPM dataset)",
        "Calculating disparity map using SGBM (PPM dataset)",
        "Calculating disparity map using custom method (PPM dataset)",
        "Loading ground truth (PGM)",
        "Cropping images (PPM & PGM)",
        "Calculating color difference maps (PPM)",
        "Calculating MSE (PPM)",
        "Calculating SSIM (PPM)",
        "Plotting disparity map comparison (PPM)",
        "Calculating disparity map using SGBM (real life dataset)",
        "Calculating disparity map using custom method (real life dataset)",
        "Cropping images (real life dataset)",
        "Plotting disparity map comparison (real life dataset)",
        "Cleaning up"
    ]

    with tqdm(
            total=len(tasks),
            desc="Processing Steps...",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",  # Processing Steps ██████-----| 45/100
            # bar_format="{l_bar}{bar}{r_bar}", # Processing Steps ██████----- 45%| ETA: 00:10
            dynamic_ncols=True,
            colour="green",
            file=stderr,
    ) as pbar:
        # Calculate the disparity map using BM
        pbar.set_description(tasks[0])
        disparityMapBM = zw.calculate_disparity_map(
            leftImagePath=img_left,
            rightImagePath=img_right,
            blockSize=9,
            numDisparities=16,
            disparityCalculationMethod="bm",
            saveDisparityMap=saveDisparityMap,
            saveDisparityMapPath=os.path.join(saveDisparityMapPath, "disparity_map_BM.png"),
            showDisparityMap=showMaps
        )
        pbar.update(1)

        # Calculate the disparity map using SGBM
        pbar.set_description(tasks[1])
        disparityMapSGBM = zw.calculate_disparity_map(
            leftImagePath=img_left,
            rightImagePath=img_right,
            blockSize=9,
            numDisparities=16,
            minDisparity=0,
            disparityCalculationMethod="sgbm",
            saveDisparityMap=saveDisparityMap,
            saveDisparityMapPath=os.path.join(saveDisparityMapPath, "disparity_map_SGBM.png"),
            showDisparityMap=showMaps
        )
        pbar.update(1)

        # Calculate the disparity map using custom block matching
        pbar.set_description(tasks[2])
        disparityMapCustom = zw.calculate_disparity_map(
            leftImagePath=img_left,
            rightImagePath=img_right,
            maxDisparity=64,
            windowSize=(11, 11),
            disparityCalculationMethod="custom",
            saveDisparityMap=saveDisparityMap,
            saveDisparityMapPath=os.path.join(saveDisparityMapPath, "disparity_map_custom.png"),
            showDisparityMap=showMaps
        )
        pbar.update(1)

        # Load the ground truth disparity map
        pbar.set_description(tasks[3])
        groundTruth = zw.load_pgm_file(groundTruthPath, disparityMapBM.shape)
        pbar.update(1)

        # Crop the images
        pbar.set_description(tasks[4])
        croppingPercentage = 0.75

        disparityMapBM = zw.crop_image(disparityMapBM, cropPercentage=croppingPercentage)
        disparityMapSGBM = zw.crop_image(disparityMapSGBM, cropPercentage=croppingPercentage)
        disparityMapCustom = zw.crop_image(disparityMapCustom, cropPercentage=croppingPercentage)
        groundTruth = zw.crop_image(groundTruth, cropPercentage=croppingPercentage)
        pbar.update(1)

        # Calculate color difference maps
        pbar.set_description(tasks[5])
        colorDiffBM = zw.calculate_color_difference_map(disparityMapBM, groundTruth)
        colorDiffSGBM = zw.calculate_color_difference_map(disparityMapSGBM, groundTruth)
        colorDiffCustom = zw.calculate_color_difference_map(disparityMapCustom, groundTruth)
        pbar.update(1)

        # Calculate MSE
        pbar.set_description(tasks[6])
        mseBM = zw.calculate_mse_disparity(disparityMapBM, groundTruth)
        mseSGBM = zw.calculate_mse_disparity(disparityMapSGBM, groundTruth)
        mseCustom = zw.calculate_mse_disparity(disparityMapCustom, groundTruth)

        print(
            "\n\nMSE:\n"
            f"\t{'mseBM':<10} = {mseBM:^10.2f}\n"
            f"\t{'mseSGBM':<10} = {mseSGBM:^10.2f}\n"
            f"\t{'mseCustom':<10} = {mseCustom:^10.2f}"
        )
        pbar.update(1)

        # Calculate SSIM
        pbar.set_description(tasks[7])
        ssimBM = zw.calculate_ssim_disparity(disparityMapBM, groundTruth)
        ssimSGBM = zw.calculate_ssim_disparity(disparityMapSGBM, groundTruth)
        ssimCustom = zw.calculate_ssim_disparity(disparityMapCustom, groundTruth)

        print(
            "\n\nSSIM:\n"
            f"\t{'ssimBM':<10} = {ssimBM:^10.2f}\n"
            f"\t{'ssimSGBM':<10} = {ssimSGBM:^10.2f}\n"
            f"\t{'ssimCustom':<10} = {ssimCustom:^10.2f}"
        )
        pbar.update(1)

        # Plot the comparison
        pbar.set_description(tasks[8])
        zw.plot_disparity_map_comparison(
            disparityMapBM=disparityMapBM,
            disparityMapSGBM=disparityMapSGBM,
            disparityMapCustom=disparityMapCustom,
            groundTruth=groundTruth,
            colorDiffMapBM=colorDiffBM,
            colorDiffMapSGBM=colorDiffSGBM,
            colorDiffMapCustom=colorDiffCustom,
            saveComparison=saveComparison,
            savePath=saveComparisonPath
        )
        pbar.update(1)

        # Calculate the disparity map using SGBM
        pbar.set_description(tasks[9])
        disparityMapSGBM = zw.calculate_disparity_map(
            leftImagePath=img_left_real_life,
            rightImagePath=img_right_real_life,
            blockSize=7,
            numDisparities=16,
            minDisparity=8,
            disparityCalculationMethod="sgbm",
            saveDisparityMap=saveDisparityMap,
            saveDisparityMapPath=os.path.join(saveDisparityMapPath, "disparity_map_SGBM_RL.png"),
            showDisparityMap=showMaps
        )
        pbar.update(1)

        # Calculate the disparity map using custom block matching
        pbar.set_description(tasks[10])
        disparityMapCustom = zw.calculate_disparity_map(
            leftImagePath=img_left_real_life,
            rightImagePath=img_right_real_life,
            maxDisparity=16,
            windowSize=(9, 9),
            disparityCalculationMethod="custom",
            saveDisparityMap=saveDisparityMap,
            saveDisparityMapPath=os.path.join(saveDisparityMapPath, "disparity_map_custom_RL.png"),
            showDisparityMap=showMaps
        )
        pbar.update(1)

        # Crop the images
        pbar.set_description(tasks[11])
        croppingPercentage = 0.75

        disparityMapSGBM = zw.crop_image(disparityMapSGBM, cropPercentage=croppingPercentage)
        disparityMapCustom = zw.crop_image(disparityMapCustom, cropPercentage=croppingPercentage)
        pbar.update(1)

        # Plot the comparison
        pbar.set_description(tasks[12])
        zw.plot_disparity_map_comparison(
            disparityMapBM=cv2.imread(img_left_real_life, cv2.IMREAD_GRAYSCALE), # top left
            disparityMapSGBM=cv2.imread(img_right_real_life, cv2.IMREAD_GRAYSCALE), # top right
            disparityMapCustom=disparityMapSGBM, # bottom left
            groundTruth=disparityMapCustom, # bottom right
            saveComparison=saveComparison,
            savePath=saveComparisonPath_RL,
            titleMain="Real Life Dataset Disparity Map Comparison",
            title1="Left Image",
            title2="Right Image",
            title3="Disparity Map using StereoSGBM",
            title4="Disparity Map using Custom Block Matching",
        )
        pbar.update(1)

        pbar.set_description(tasks[13])

    print(Fore.GREEN + "\n\nAll steps completed successfully")


if __name__ == '__main__':
    main()