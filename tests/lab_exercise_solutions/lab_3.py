import zaowr_polsl_kisiel as zw

from sys import stdout
import os
from colorama import Fore, Style, init as colorama_init  # , Back
from tqdm import tqdm  # progress bar

colorama_init(autoreset=True)

if __name__ == '__main__':
    # Paths to the images
    img_left = "data/left.pgm"
    img_right = "data/right.pgm"

    groundTruthPath = "data/disp2.pgm"

    showMaps = True
    saveDisparityMap = True
    saveDisparityMapPath = "data/"

    saveComparison = True
    saveComparisonPath = "data/comparison.png"


    tasks = [
        "Calculating disparity map using BM",
        "Calculating disparity map using SGBM",
        "Calculating disparity map using custom method",
        "Loading ground truth",
        "Cropping images",
        "Calculating color difference maps",
        "Calculating MSE",
        "Calculating SSIM",
        "Plotting disparity map comparison"
        "Cleaning up"
    ]

    with tqdm(
        total=len(tasks),
        desc="Processing Steps...",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}", # Processing Steps ██████-----| 45/100
        # bar_format="{l_bar}{bar}{r_bar}", # Processing Steps ██████----- 45%| ETA: 00:10
        dynamic_ncols=True,
        colour="green",
        file=stdout
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
        pbar.update(1)

        # Calculate SSIM
        pbar.set_description(tasks[7])
        ssimBM = zw.calculate_ssim_disparity(disparityMapBM, groundTruth)
        ssimSGBM = zw.calculate_ssim_disparity(disparityMapSGBM, groundTruth)
        ssimCustom = zw.calculate_ssim_disparity(disparityMapCustom, groundTruth)
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
        pbar.set_description(tasks[9])

    print(Fore.GREEN + "\n\nAll steps completed successfully")