import numpy as np
from colorama import Fore, Style, init as colorama_init  # , Back

colorama_init(autoreset=True)

def disparity_to_depth_map(
        disparityMap: np.ndarray,
        baseline: float,
        focalLength: float,
        aspect: float = 1.0
) -> np.ndarray:
    """
    Convert disparity map to depth map.

    :param np.ndarray disparityMap: Disparity map
    :param float baseline: Baseline
    :param float focalLength: Focal length
    :param float aspect: Aspect ratio

    :raises ValueError: Raises ValueError if:
        - **`disparityMap`** is not a numpy array
        - **`baseline`** is not a positive number
        - **`focalLength`** is not a positive number

    :raises TypeError: Raises TypeError if:
        - **`baseline`** or **`focalLength`** or **`aspect`** is not a float

    :return: Depth map as a numpy array
    """
    if disparityMap is None or not isinstance(disparityMap, np.ndarray):
        raise ValueError(Fore.RED + "\nDisparity map must be provided!\n")

    if baseline is None or baseline <= 0.0:
        raise ValueError(Fore.RED + "\nBaseline must be provided!\n")

    if focalLength is None or focalLength <= 0.0:
        raise ValueError(Fore.RED + "\nFocal length must be provided!\n")

    if not isinstance(baseline, float) or not isinstance(focalLength, float) or not isinstance(aspect, float):
        raise ValueError(Fore.RED + "\nBaseline, focal length and aspect ratio must be floats!\n")

    # Convert disparity to depth
    disparityMap = np.float32(disparityMap)

    # Adjust disparity with offset
    valid_disparity = disparityMap > 0  # Only consider valid disparity values
    adjusted_disparity = disparityMap
    depth_map = np.zeros_like(disparityMap)
    depth_map[valid_disparity] = baseline * focalLength / adjusted_disparity[valid_disparity]

    depth_map = depth_map / aspect # to meters

    return depth_map