# TODO list

1. Mono calibration:
   - [x] Calibration with Charuco pattern,
   - [x] List of images where the pattern was properly detected,
   - [x] Update the params class,

2. Stereo calibration:
   - [x] Calculate FOV,
   - [x] Calibration with Charuco pattern,
   - [x] Add corresponding lines after calibration,
   - [x] Add docstrings,
   - [x] Add exception handling,
   - [x] Save / Load configuration,
   - [x] Add stereo calibration params class (load),
   - [x] Separate functions for rectification etc.,
   - [x] Add different interpolation methods and option to save those images,

3. Disparity maps:
   - [x] Check for bugs,
   - [x] Check if anything can be simplified,
   - [x] UPDATE THE DOCS!
     - [x] load_pgm_file(),
     - [x] calculate_disparity_map(),
     - [x] save_disparity_map(),
     - [x] calculate_color_difference_map(),
     - [x] crop_image(),
     - [x] calculate_mse_disparity(),
     - [x] calculate_ssim_disparity(),
     - [x] plot_disparity_map_comparison(),
   - [x] Calculate disparity map,
   - [x] Add different algorithms for disparity map calculation,
   - [x] Calculate color difference map,
   - [x] Add docstrings,
   - [x] Add exception handling,
   - [x] Save / Load configuration,
   - [x] Add code requirements,

4. Depth maps:
   - [x] Check for bugs,
   - [x] Check if anything can be simplified ???,
   - [x] Prepare the outline of the code,
   - [x] Add docstrings,
   - [x] Add exception handling,
   - [x] Load provided configuration (and validate it),
   - [x] Add code requirements,
   - [x] Check the `__init__` files,
   - [x] Check if any new functions have to be added,
   - [x] UPDATE THE DOCS!
     - [x] load_depth_map_calibration(),
     - [x] load_pfm_file(),
     - [x] write_ply_file(),
     - [x] decode_depth_map(),
     - [x] depth_map_normalize(),
     - [x] depth_to_disparity_map(),
     - [x] disparity_map_normalize(),
     - [x] disparity_to_depth_map(),
     - [x] display_img_plt(),
     - [x] compare_images(),

5. Exam fixes:
   - [x] Function to get pixel coordinates from an image,
   - [x] Function to get map value for points (e.g. disparity, depth) (get pixel coordinates -> get map value for that pixel),
   - [x] Function to create a point cloud,
   - [] UPDATE THE DOCS!
     - [] get_image_points(),
     - [] get_map_value_for_points(),
     - [] create_color_point_cloud(),

6. Optical flow:
   - [x] sparse optical flow,
   - [x] dense optical flow,
   - [x] list available camera ports,
   - [x] read images from folder,
   - [?] detect movement and its direction (DONE WITH SIMPLE CLUSTERING - NOT SURE IF CORRECT),
   - [?] detect movement from camera feed (DONE WITH SIMPLE CLUSTERING - NOT SURE IF CORRECT),
   - [] UPDATE THE DOCS!
     - [] list_camera_ports_available()
     - [] read_images_from_folder()
     - [] sparse_optical_flow()
     - [] dense_optical_flow()
     - [] configure_qt_platform()

7. Misc.:
   - [] Clean the USAGE.md file !!!,
   - [x] Add function to validate / load params stored in files,
   - [x] Add requirements based on the tasks provided,
   - [x] Add directory with lab solutions,
   - [x] Divide code into modules,
   - [x] Add docstrings to all functions, classes and modules,
   - [x] Unit tests for core functions,
   - [NAH...] Unit tests for content loaders ???,
