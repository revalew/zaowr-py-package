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
   - [] Check for bugs,
   - [] Check if anything can be simplified,
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

4. Misc.:
   - [x] Add function to validate / load params stored in files,
   - [x] Add requirements based on the tasks provided,
   - [x] Add directory with lab solutions,
   - [x] Divide code into modules,
   - [x] Add docstrings to all functions, classes and modules,
   - [x] Unit tests for core functions,
   - [] Unit tests for content loaders ???,
