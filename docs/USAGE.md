# RTFM - Use Cases for zaowr_polsl_kisiel and the importance of docstrings

<br/>
<br/>

## Table of Contents

1. [`Docstrings`](#docstrings)
2. [`@measure_perf decorator`](#measure_perf-decorator)
3. [`calibrate_camera()`](#calibrate_camera)
4. [`are_params_valid()`](#are_params_valid)
5. [`remove_distortion()`](#remove_distortion)
6. [`stereo_calibration()`](#stereo_calibration)
7. [`calculate_fov()`](#calculate_fov)
8. [`stereo_rectify()`](#stereo_rectify)
9. [`find_aruco_dict()`](#find_aruco_dict)
10. [`load_calibration()`](#load_calibration)
11. [`load_rectification_maps()`](#load_rectification_maps)
12. [`load_stereo_calibration()`](#load_stereo_calibration)
13. [`save_calibration()`](#save_calibration)
14. [`load_pgm_file()`](#load_pgm_file)
15. [`calculate_disparity_map()`](#calculate_disparity_map)
16. [`save_disparity_map()`](#save_disparity_map)
17. [`calculate_color_difference_map()`](#calculate_color_difference_map)
18. [`crop_image()`](#crop_image)
19. [`calculate_mse_disparity()`](#calculate_mse_disparity)
20. [`calculate_ssim_disparity()`](#calculate_ssim_disparity)
21. [`plot_disparity_map_comparison()`](#plot_disparity_map_comparison) 

<br/>
<br/>

### Docstrings

Using Python Docstrings to Enhance Understanding

In Python, docstrings are a way to provide documentation for your functions, classes, and modules. They explain what your code does, what each parameter does, what is returned and how to use it. They are written between triple quotes (""") and are often used to explain the purpose of a function, class, or module.

<ul>
<li> In IDEs or Text Editors: Many modern Integrated Development Environments (IDEs) and text editors, such as PyCharm, Visual Studio Code, or Jupyter Notebook, allow you to hover your mouse over a function to see its description provided by the docstring. Similarly, hovering over a parameter will display information about what that parameter does (if it is described in the docstring).

</li>
<br/>
<li> In the Terminal: You can read docstrings in the terminal using the help() function, which prints the docstring to the console.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

# Display documentation for the entire module
help(zw)

# Display specific submodule's documentation
help(zw.calibration)

# Display detailed documentation for a specific function
help(zw.calibrate_camera)
```

</li>
</ul>
<br/>
<br/>

### `@measure_perf` decorator

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Example usage

After importing the package we can use the `@measure_perf` decorator to measure the performance of a function. The decorator will print the function name and the time it takes to run.

We can also save the results to a file using the `output_file` parameter (`@measure_perf(output_file="perf_results.txt")`).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

@zw.measure_perf
def my_function():
    pass

my_function()
```

</li>
<br/>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>

<br/>
<br/>

### `calibrate_camera()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calibrate_camera(
    chessBoardSize: tuple[int, int],
    squareRealDimensions: float,
    calibImgDirPath: str,
    globImgExtension: str = "png",
    saveCalibrationParams: bool = False,
    calibrationParamsPath: str = "",
    displayFoundCorners: bool = False,
    displayMSE: bool = False,
    improveSubPix: bool = True,
    showListOfImagesWithChessboardFound: bool = False,
    terminationCriteria: tuple[Any, int, float] = (
        cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER,
        30,
        0.001,
    ),
    useCharuco: bool = False,
    charucoDictName: str = "DICT_6X6_250",
    markerLength: float = 20.0,
    displayIds: bool = False,
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calibrate a MONO camera.
As a result, the camera matrix, distortion coefficients, and rotation and translation vectors are saved to a JSON file, which can be used later to process images.

To properly calibrate the camera, we have to specify the number of inner corners, the real-world dimension of one side of a square, and the path to the calibration images.

Before running the function we have to check the image extensions and image paths. If the extensions are not the same, an error will be raised and the function will fail.

When we want to save the calibration parameters, we also have to specify the path to the file where we want to save them and enable the `saveCalibrationParams` parameter.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

imgPath = "./ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/"

zw.calibrate_camera(
    chessBoardSize=(10, 7), # NUMBER OF INNER CORNERS
    squareRealDimensions=28.67, # mm
    calibImgDirPath=imgPath, # PATH TO CALIBRATION IMAGES
    saveCalibrationParams=True, # SAVE CALIBRATION PARAMETERS
    calibrationParamsPath=calibrationFile, # PATH TO CALIBRATION PARAMETERS
    displayFoundCorners=True, # DISPLAY FOUND CORNERS
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `are_params_valid()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def are_params_valid(path: str) -> tuple[bool, dict[str, Any] | None]
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to check if the calibration parameters are valid. If they are not valid, we can calibrate the camera and save the new parameters. If they are valid, we can skip the calibration and use them to process images quickly.

If the parameters are valid, the function returns `True` and the parameters as a `tuple[bool, dict[str, Any]]` and if they are not valid, the function returns `False` and `None`. If validation fails, an error will be raised.

This function **WILL NOT** provide type hints for the returned dictionary (as opposed to the `load_calibration`, `load_rectification_maps`, and `load_stereo_calibration` functions).

To check if the parameters are valid, we have to specify the path to the file where we saved them.

If the file does not exist, an error will be raised and the function will return `False` and `None` but the program will not exit.

After calibrating the camera, we can use the `are_params_valid` function to check if the new parameters are valid and exit the program if they are not.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

imgPath = "./ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/"

sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

if not sub_valid:
    zw.calibrate_camera(
        chessBoardSize=(10, 7),
        squareRealDimensions=28.67,
        calibImgDirPath=imgPath,
        saveCalibrationParams=True,
        calibrationParamsPath=calibrationFile,
        displayFoundCorners=False,
    )

    sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

    if not sub_valid:
        raise RuntimeError("Calibration failed. Parameters are still invalid.")
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `remove_distortion()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def remove_distortion(
    cameraMatrix: Any,
    distortionCoefficients: Any,
    imgToUndistortPath: str,
    showImgToUndistort: bool = False,
    showUndistortedImg: bool = False,
    saveUndistortedImg: bool = False,
    undistortedImgPath: str = "",
    undistortionMethod: str = "undistort",
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to remove distortion from an image. As a result, we get an undistorted image.

To remove distortion from an image, we have to specify the camera matrix, distortion coefficients, and the path to the image to be undistorted. The calibration params must be valid, and we can use the `are_params_valid` function to check if they are valid and load them.

If we want to save the undistorted image, we also have to specify the path to the directory where we want to save it and enable the `saveUndistortedImg` parameter. The file will be saved with the name `{original_image_name}_undistorted{original_file_extension}`. If the directory does not exist, it will be created.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

imgToUndistort = "./tests/undistorted/distorted.png"

undistortedImgPath = "./tests/undistorted/"

sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

if sub_valid:
    zw.remove_distortion(
        cameraMatrix=calibrationParams1["cameraMatrix"],
        distortionCoefficients=calibrationParams1["distortionCoefficients"],
        imgToUndistortPath=imgToUndistort,
        saveUndistortedImg=True,
        undistortedImgPath=undistortedImgPath,
    )
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `stereo_calibration()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def stereo_calibration(
    chessBoardSize: tuple[int, int],
    squareRealDimensions: float,
    calibImgDirPath_left: str,
    calibImgDirPath_right: str,
    globImgExtension: str = "png",
    saveCalibrationParams: bool = False,
    loadCalibrationParams: bool = False,
    calibrationParamsPath_left: str = "",
    calibrationParamsPath_right: str = "",
    saveStereoCalibrationParams: bool = False,
    stereoCalibrationParamsPath: str = "",
    displayFoundCorners: bool = False,
    displayMSE: bool = False,
    improveSubPix: bool = True,
    showListOfImagesWithChessboardFound: bool = False,
    terminationCriteria: tuple[Any, int, float] = (
        cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER,
        30,
        0.001
    ),
    stereoCalibrationFlags: Any = cv.CALIB_FIX_INTRINSIC,
    useCharuco: bool = False,
    charucoDictName: str = "DICT_6X6_250",
    markerLength: float = 20.0,
    displayIds: bool = False,
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calibrate the stereo camera. As a result, we get 3 files with stereo calibration parameters and the left and right camera calibration parameters.

To properly calibrate the stereo camera, we have to specify the number of inner corners, the real-world dimension of one side of a square, and the paths to the left and right calibration images.

Before running the function we have to check the image extensions and image paths. If the extensions are not the same, an error will be raised and the function will fail.

After calibrating the stereo camera, we can use the `are_params_valid` function to check if the new parameters are valid and exit the program if they are not.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

left_cam = "./ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam1/"
right_cam = "./ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam4/"

left_cam_params_stereo = "./tests/stereo_calibration_params/left_params.json"
right_cam_params_stereo = "./tests/stereo_calibration_params/right_params.json"
stereo_cam_params = "./tests/stereo_calibration_params/stereo_params.json"

left_valid, params_left = zw.are_params_valid(left_cam_params_stereo)
right_valid, params_right = zw.are_params_valid(right_cam_params_stereo)
stereo_valid, stereo_params = zw.are_params_valid(stereo_cam_params)

if not left_valid or not right_valid or not stereo_valid:
    # hover over function parameters to see what they do (if names are not enough...)
    zw.stereo_calibration(
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
    left_valid, params_left = zw.are_params_valid(left_cam_params_stereo)
    right_valid, params_right = zw.are_params_valid(right_cam_params_stereo)
    stereo_valid, stereo_params = zw.are_params_valid(stereo_cam_params)

    # Check again to ensure parameters are valid
    if not left_valid or not right_valid or not stereo_valid:
        raise RuntimeError("Calibration failed. Parameters are still invalid.")
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `calculate_fov()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calculate_fov(cameraMatrix: np.ndarray, imageSize: tuple[float, float]) -> tuple[float, float]
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate the field of view (FOV) of the camera. As a result, we get the horizontal and vertical FOV.

To calculate the FOV, we have to specify the camera matrix and the image size. The image size is the size of one of the images in the calibration images. And the camera matrix can be found in the calibration parameters.

<br/>
<br/>

```python
import cv2
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

imgPath = "./ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/1.png"

imgSize = cv2.cvtColor(cv2.imread(imgPath), cv2.COLOR_BGR2GRAY).shape[::-1]
# OR imgSize = cv2.imread(imgPath).shape[2:][::-1]

sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

if sub_valid:
    fov_horizontal, fov_vertical = zw.calculate_fov(
        cameraMatrix=calibrationParams1["cameraMatrix"],
        imageSize=imgSize,
    )
    print(f"Horizontal fov: {fov_horizontal:.2f} degrees")
    print(f"Vertical fov: {fov_vertical:.2f} degrees")
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `stereo_rectify()`

[Back to the top (TOC))](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def stereo_rectify(
    calibImgDirPath_left: str,
    calibImgDirPath_right: str,
    cameraMatrix_left: np.ndarray = None,
    cameraMatrix_right: np.ndarray = None,
    distortionCoefficients_left: np.ndarray = None,
    distortionCoefficients_right: np.ndarray = None,
    R: np.ndarray = None,
    T: np.ndarray = None,
    F: np.ndarray = None,
    imgPoints_left: np.ndarray = None,
    imgPoints_right: np.ndarray = None,
    whichImage: int = 0,
    saveRectifiedImages: bool = False,
    rectifiedImagesDirPath: str = "./rectifiedImages",
    globImgExtension: str = "png",
    showRectifiedImages: bool = False,
    loadStereoCalibrationParams: bool = False,
    stereoCalibrationParamsPath: str = "",
    saveRectificationMaps: bool = False,
    loadRectificationMaps: bool = False,
    rectificationMapsPath: str = "",
    testInterpolationMethods: bool = False,
    drawEpipolarLinesParams: tuple[int, int, int] = (15, 2, 2),
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to rectify the stereo images. As a result, we get 3 files with stereo rectified images.

To properly rectify the stereo images, we have to specify the paths to the left and right calibration images, as well as the paths to the stereo, left and right calibration parameters and the path to the directory where we want to save the rectified images. If the directory for rectified images does not exist, it will be created.

Best practices are to calibrate the stereo camera first and then rectify the images. We can load the stereo calibration parameters in the main function and pass them to the `stereo_rectify` function, or we can pass the paths to the stereo calibration parameters and enable the `loadStereoCalibrationParams` parameter. 

Before running the function we have to check the image extensions and image paths. If the extensions are not the same, an error will be raised and the function will fail.

We can specify the parameters for drawing the epipolar lines - the number of lines, the thickness of the lines, and the thickness of the ROI with the `drawEpipolarLinesParams` parameter.

`whichImage` parameter is used to specify which image to rectify. By default, it is set to 0, which means that the first set of images in the `left_cam` and `right_cam` directories will be rectified. Sometimes `glob` function can change the order ot the images in the list (in my case, `0` was actually `28.png` and not `1.png`).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

left_cam = "./ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam1/"
right_cam = "./ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam4/"

left_cam_params_stereo = "./tests/stereo_calibration_params/left_params.json"
right_cam_params_stereo = "./tests/stereo_calibration_params/right_params.json"
stereo_cam_params = "./tests/stereo_calibration_params/stereo_params.json"

rectified_images_dir = "./tests/stereo_rectified_images/"

left_valid, params_left = zw.are_params_valid(left_cam_params_stereo)
right_valid, params_right = zw.are_params_valid(right_cam_params_stereo)
stereo_valid, stereo_params = zw.are_params_valid(stereo_cam_params)

if left_valid and right_valid and stereo_valid:
    zw.stereo_rectify(
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
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `find_aruco_dict()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def find_aruco_dict(imgPath) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to find the aruco dictionary used by the calibration board. 

This function will print the dictionary names and the number of markers found in that dictionary to the console.

e.g.
    "[INFO] detected 4 markers for '4X4_50'"
    "[INFO] detected 44 markers for '6X6_50'"
    "[INFO] detected 44 markers for '6X6_100'"
    "[INFO] detected 44 markers for '6X6_250'"
    "[INFO] detected 44 markers for '6X6_1000'"

We should choose the dictionary with the highest number of markers found and lowest number of IDs in that dictionary - "6X6_100" means that the ArUco markers are 6x6 and have 100 IDs. Each charuco board should come with detailed information about the size, square size, marker size and the dictionary type [e.g. here](../tests/charuco_tests/charuco_details.jpg).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

imgPath = "./ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/1.png"

zw.find_aruco_dict(imgPath)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `load_calibration()`

[Back to the top (TOC))](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
class CalibrationParams(TypedDict):
    mse: float
    rms: float
    objPoints: np.ndarray
    imgPoints: np.ndarray
    cameraMatrix: np.ndarray
    distortionCoefficients: np.ndarray
    rotationVectors: list
    translationVectors: list


def load_calibration(calibrationParamsPath: str) -> CalibrationParams
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to load the calibration parameters from a JSON file and return them as a `dict[str, Any]`.

This function will provide type hints for the returned dictionary.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

calibrationParams1 = zw.load_calibration(calibrationFile)

mse = calibrationParams1["mse"]
rms = calibrationParams1["rms"]
# ...
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `load_rectification_maps()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
class RectificationMaps(TypedDict):
    map1_left: np.ndarray
    map2_left: np.ndarray
    map1_right: np.ndarray
    map2_right: np.ndarray


def load_rectification_maps(rectificationMapsPath: str) -> RectificationMaps
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to load the rectification maps from a JSON file and return them as a `dict[str, Any]`.

This function will provide type hints for the returned dictionary.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

rectificationMapsFile = "./tests/rectification_maps/rectification_maps.json"

rectificationMaps = zw.load_rectification_maps(rectificationMapsFile)

map1_left = rectificationMaps["map1_left"]
map2_left = rectificationMaps["map2_left"]
# ...
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `load_stereo_calibration()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
class StereoCalibrationParams(TypedDict):
    reprojectionError: float
    fov_left: tuple[float, float]
    fov_right: tuple[float, float]
    baseline: float
    cameraMatrix_left: np.ndarray
    distortionCoefficients_left: np.ndarray
    cameraMatrix_right: np.ndarray
    distortionCoefficients_right: np.ndarray
    rotationMatrix: np.ndarray
    translationVector: np.ndarray
    essentialMatrix: np.ndarray
    fundamentalMatrix: np.ndarray


def load_stereo_calibration(calibrationParamsPath: str) -> StereoCalibrationParams
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to load the stereo calibration parameters from a JSON file and return them as a `dict[str, Any]`.

This function will provide type hints for the returned dictionary.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/stereo_calibration_params/stereo_params.json"

stereoParams = zw.load_stereo_calibration(calibrationFile)

reprojectionError = stereoParams["reprojectionError"]
fov_left = stereoParams["fov_left"]
# ...
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `save_calibration()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def save_calibration(
    calibrationParams: dict[str, list | Any], calibrationParamsPath: str
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to save the calibration parameters to a JSON file OR use it to save the dictionary to a JSON file.

If the directory in the `calibrationParamsPath` does not exist, it will be created.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

calibrationParams = zw.load_calibration(calibrationFile)

zw.save_calibration(calibrationParams, calibrationFile)

# OR

distorted_params = {
    "k1": calibrationParams["distortionCoefficients"][0][0],
    "k2": calibrationParams["distortionCoefficients"][0][1],
    "p1": calibrationParams["distortionCoefficients"][0][2],
    "p2": calibrationParams["distortionCoefficients"][0][3],
    "k3": calibrationParams["distortionCoefficients"][0][4],
}

zw.save_calibration(distorted_params, "./tests/distorted_params/distorted_params.json")
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `load_pgm_file()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def load_pgm_file(
        pgmPath: str,
        targetShape: tuple[int, int]
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to load a PGM file and return it as a numpy array. The function also resizes the image to the specified shape (usually the shape of the calculated disparity map).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

pgmPath = "./tests/disparity_maps/ground_truth.pgm"

groundTruth = zw.load_pgm_file(pgmPath, targetShape=(512, 512))
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `calculate_disparity_map()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calculate_disparity_map(
    leftImagePath: str,
    rightImagePath: str,
    blockSize: int = 9, # for StereoBM, StereoSGBM & Custom 2
    numDisparities: int = 16, # for StereoBM & StereoSGBM
    minDisparity: int = 0, # for StereoSGBM
    maxDisparity: int = 64, # for Custom 1 & Custom 2
    windowSize: tuple[int, int] = (11, 11), # for Custom 1
    disparityCalculationMethod: str = "bm",
    saveDisparityMap: bool = False,
    saveDisparityMapPath: str = None,
    showDisparityMap: bool = False
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate the disparity map and optionally save it and/or show it. We have to specify the path to the left and right images (**already rectified images!**), the block size, the number of disparities, the minimum disparity, the maximum disparity, the window size, the disparity calculation method, the save disparity map and/or show disparity map parameters.

We can choose the disparity calculation method between StereoBM, StereoSGBM, Custom 1 and Custom 2. Depending on the disparity calculation method, we have to specify different parameters.

We can also show the map using the `showDisparityMap` parameter with or without saving.

<br/>
<br/>

```python
import os
import zaowr_polsl_kisiel as zw

disparityMapSGBM = zw.calculate_disparity_map(
            leftImagePath="left.png", # path to the left image
            rightImagePath="right.png", # path to the right image
            blockSize=9, # block size for StereoBM & StereoSGBM
            numDisparities=16, # number of disparities for StereoBM & StereoSGBM
            minDisparity=0, # minimum disparity for StereoSGBM
            disparityCalculationMethod="sgbm", # use StereoSGBM for disparity calculation
            saveDisparityMap=True, # save the disparity map
            saveDisparityMapPath=os.path.join("./tests/disparity_maps", "disparity_map_SGBM.png"), # path to save the disparity map
            showDisparityMap=True # show the disparity map
        )
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `save_disparity_map()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def save_disparity_map(
    disparityMap: np.ndarray,
    savePath: str,
    show: bool = False,
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to save a disparity map as a PNG file and optionally show it.

We can save the disparity map to a file using the `saveDisparityMap` parameter (and `saveDisparityMapPath`) directly in the function `calculate_disparity_map()` (**recommended**). 

We can also show the map using the `show` parameter with or without saving.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

disparityMap = zw.calculate_disparity_map(
    leftImagePath="./tests/disparity_maps/left.png",
    rightImagePath="./tests/disparity_maps/right.png",
)

zw.save_disparity_map(
    disparityMap=disparityMap,
    savePath="./tests/disparity_maps/disparity_map.png",
    show=True
)

#######################
# OR (RECOMMENDED)
#######################

disparityMap = zw.calculate_disparity_map(
    leftImagePath="./tests/disparity_maps/left.png",
    rightImagePath="./tests/disparity_maps/right.png",
    saveDisparityMap=True, # set saveDisparityMap to True
    saveDisparityMapPath="./tests/disparity_maps/disparity_map.png", # desired path to save
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `calculate_color_difference_map()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calculate_color_difference_map(
        disparityMap: np.ndarray,
        groundTruth: np.ndarray
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate the color difference map and return it as a numpy array. We have to specify the disparity map and the ground truth image. The disparity map is calculated using the `calculate_disparity_map()` function and the ground truth image is loaded using the `load_pgm_file()` function.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import os

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
groundTruth = zw.load_pgm_file(groundTruthPath, disparityMapBM.shape)
colorDiffBM = zw.calculate_color_difference_map(disparityMapBM, groundTruth)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `crop_image()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def crop_image(
        img: np.ndarray,
        cropPercentage: float = 0.75
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to crop an image and return it as a numpy array. We have to specify the image and the percentage of the image to crop.

Image is cropped from the top, bottom, left and right to retain only a certain percentage of the original image (75% by default).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import os

groundTruth = zw.load_pgm_file("./tests/disparity_maps/ground_truth.pgm")
groundTruth = zw.crop_image(groundTruth, cropPercentage=0.75)

# AND

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
disparityMapBM = zw.crop_image(disparityMapBM, cropPercentage=0.75)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `calculate_mse_disparity()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calculate_mse_disparity(
        map1: np.ndarray,
        map2: np.ndarray
) -> float
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate the **Mean Squared Error (MSE)** of two disparity maps and return it as a float. We have to specify the two disparity maps to compare - the ground truth and the calculated disparity map. Images are cropped before calculating the MSE.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import os

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
groundTruth = zw.load_pgm_file("./tests/disparity_maps/ground_truth.pgm", disparityMapBM.shape)

groundTruth = zw.crop_image(groundTruth, cropPercentage=0.75)
disparityMapBM = zw.crop_image(disparityMapBM, cropPercentage=0.75)

mseBM = zw.calculate_mse_disparity(disparityMapBM, groundTruth)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `calculate_ssim_disparity()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calculate_ssim_disparity(
        map1: np.ndarray,
        map2: np.ndarray
) -> float
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate the **Structural Similarity Index (SSIM)** of two disparity maps and return it as a float. We have to specify the two disparity maps to compare - the ground truth and the calculated disparity map. Images are cropped before calculating the SSIM.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import os

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
groundTruth = zw.load_pgm_file("./tests/disparity_maps/ground_truth.pgm", disparityMapBM.shape)

groundTruth = zw.crop_image(groundTruth, cropPercentage=0.75)
disparityMapBM = zw.crop_image(disparityMapBM, cropPercentage=0.75)

ssimBM = zw.calculate_ssim_disparity(disparityMapBM, groundTruth)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `plot_disparity_map_comparison()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def plot_disparity_map_comparison(
    disparityMapBM: np.ndarray,
    disparityMapSGBM: np.ndarray,
    disparityMapCustom: np.ndarray,
    groundTruth: np.ndarray,
    colorDiffMapBM: np.ndarray = None,
    colorDiffMapSGBM: np.ndarray = None,
    colorDiffMapCustom: np.ndarray = None,
    showComparison: bool = False,
    saveComparison: bool = False,
    savePath: str = None
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to plot the comparison of three disparity maps and the ground truth. Before plotting we have to calculate the disparity maps and the color difference maps.

We can save the comparison to a file using the `saveComparison` parameter (and `savePath`) directly in the function `plot_disparity_map_comparison()` (**recommended**).

We can also show the comparison using the `showComparison` parameter with or without saving.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import os

disparityMapBM = zw.calculate_disparity_map(...)
disparityMapSGBM = zw.calculate_disparity_map(...)
disparityMapCustom = zw.calculate_disparity_map(...)

groundTruth = zw.load_pgm_file("./ground_truth.pgm", disparityMapBM.shape)

colorDiffMapBM = zw.calculate_color_difference_map(disparityMapBM, groundTruth)
colorDiffMapSGBM = zw.calculate_color_difference_map(disparityMapSGBM, groundTruth)
colorDiffMapCustom = zw.calculate_color_difference_map(disparityMapCustom, groundTruth)

zw.plot_disparity_map_comparison(
    disparityMapBM=disparityMapBM,
    disparityMapSGBM=disparityMapSGBM,
    disparityMapCustom=disparityMapCustom,
    groundTruth=groundTruth,
    colorDiffMapBM=colorDiffMapBM,
    colorDiffMapSGBM=colorDiffMapSGBM,
    colorDiffMapCustom=colorDiffMapCustom,
    showComparison=True
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>