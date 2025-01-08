"""
This package provides tools and utilities for camera calibration, stereo calibration,
image processing, and related operations.

Modules:

- `calibration`: Tools for single and stereo camera calibration.

- `content_loaders`: Functions to load and validate calibration data from files, load the ground truth `.pgm` or `.pfm` file,  save the disparity map, write a .ply file and load depth map calibration.

- `custom_exceptions`: Custom exceptions for error handling.

- `image_processing`: Utilities for image rectification, distortion removal, disparity map calculation, color difference map calculation, disparity map comparison, depth map conversion (disparity to depth), disparity map normalization, depth map normalization, depth map to disparity map conversion and depth map decoding.

- `tools`: Additional tools, such as ArUco dictionary identification, performance measurement, image cropping, and image display using matplotlib.

Status: Development

Year of development: 2024/2025

Author: Maksymilian Kisiel

Institution: Silesian University of Technology

Faculty: Faculty of Automatic Control, Electronics and Computer Science

Major: Informatics, master degree

Specialization: Interactive Three-Dimensional Graphics (IGT, pol. Interaktywna Grafika Trójwymiarowa, https://www.polsl.pl/rau6/en/igt-specjalization/)
"""

__version__ = "0.0.31"
__status__ = "Development"  # Allowed: "Prototype", "Beta", "Stable"

__all__ = [
    "calibration",
    "content_loaders",
    "exceptions",
    "image_processing",
    "tools",
]

# IMPORT SUBMODULES
from . import calibration
from .calibration import (
    calibrate_camera, # calibrate single camera
    stereo_calibration, # stereo calibration
    calculate_fov, # calculate fov - horizontal and vertical
)

from . import custom_exceptions
from .custom_exceptions import exceptions # custom_exceptions

from . import content_loaders
from .content_loaders import (
    are_params_valid, # validate calibration parameters stored in files and return them if valid
    save_calibration, # save calibration parameters (used for all types of params - single, stereo, rectification)
    load_calibration, # load calibration parameters for single camera
    load_stereo_calibration, # load stereo calibration
    load_rectification_maps, # load rectification maps
    save_disparity_map, # save disparity map
    load_pgm_file, # load the ground truth .pgm file
    load_pfm_file, # load the ground truth .pfm file
    write_ply_file, # write .ply file
    load_depth_map_calibration, # load depth map calibration
)

from . import image_processing
from .image_processing import (
    remove_distortion, # remove distortion from single image
    stereo_rectify, # rectify stereo image after stereo calibration
    calculate_disparity_map, # calculate disparity map using StereoBM, StereoSGBM, Custom Block Matching
    calculate_color_difference_map, # calculate color difference map
    plot_disparity_map_comparison, # plot disparity map comparison
    disparity_to_depth_map, # convert disparity map to depth map
    disparity_map_normalize, # normalize disparity map to a specified range
    depth_map_normalize, # normalize depth map to a specified range
    depth_to_disparity_map, # convert depth map to disparity map
    decode_depth_map, # decode depth map
)

from . import tools
from .tools import (
    find_aruco_dict, # find aruco dictionary if we don't know
    measure_perf, # measure performance
    calculate_mse_disparity, # calculate MSE between two disparity maps
    calculate_ssim_disparity, # calculate SSIM between two disparity maps
    crop_image, # crop image to retain only the center part (specified by percentage)
    display_img_plt, # display the image using matplotlib
    compare_images, # compare multiple images
)