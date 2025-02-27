import numpy as np
from colorama import Fore, Style, init as colorama_init  # , Back

colorama_init(autoreset=True)

def decode_depth_map(
        depthMap: np.ndarray,
        maxDepth: float = 1000.0,
        decodeDepthMapRange: str = "24-bit"
) -> np.ndarray:
    """
    Decode depth map.

    **WARNING: THIS FUNCTION WAS NOT TESTED THOROUGHLY**

    8-BIT AND 16-BIT RANGES WERE GENERATED BY JetBrains AI

    **USE ONLY THE 24-BIT RANGE**, AS OTHER RANGES MAY BE INCORRECT (MOST DEFINITELY ARE WRONG...)

    I'm only sure that the 24-bit range is correct and added the rest only for the sake of completeness

    :param np.ndarray depthMap: Depth map
    :param float maxDepth: Maximum depth
    :param str decodeDepthMapRange: Range to decode depth map to (e.g. **"8-bit"**, **"16-bit"**, **"24-bit"**)

    :raises ValueError: Raises ValueError if:
        - **`depthMap`** is not a numpy array
        - **`decodeDepthMapRange`** is not a string

    :raises TypeError: Raises TypeError if:
        - **`decodeDepthMapRange`** is not a string

    :raises RuntimeError: Raises RuntimeError if:
        - **`decodedDepthMap`** is None

    :return: Decoded depth map as a numpy array
    """

    if decodeDepthMapRange is None or not isinstance(decodeDepthMapRange, str):
        raise TypeError(Fore.RED + "\n`decodeDepthMapRange` must be a string!\n")

    if depthMap is None or not isinstance(depthMap, np.ndarray):
        raise ValueError(Fore.RED + "\nDepth map must be provided as a numpy array!\n")

    if decodeDepthMapRange not in ["8-bit", "16-bit", "24-bit"]:
        raise ValueError(Fore.RED + "\n`decodeDepthMapRange` must be '24-bit'!\n")

    # WARNING: THIS FUNCTION WAS NOT TESTED THOROUGHLY
    # GENERATED BY JetBrains AI
    # USE ONLY THE 24-BIT RANGE, AS OTHER RANGES MAY BE INCORRECT (MOST DEFINITELY ARE WRONG...)
    # I'm only sure that the 24-bit range is correct and added the rest only for the sake of completeness
    depthMapDecoded = None
    if decodeDepthMapRange == "8-bit":
        # Decode 8-bit depth map
        depthMap = depthMap[:, :, 0]
        depthMap = depthMap[:, :, ::-1]
        # Decode 8-bit depth map
        depthMapDecoded = (depthMap / 255) * maxDepth

    elif decodeDepthMapRange == "16-bit":
        # Decode 16-bit depth map
        depthMap = depthMap[:, :, :2]
        depthMap = depthMap[:, :, ::-1]
        # Decode 16-bit depth map
        R = (depthMap[:, :, 0]).astype(np.uint16)
        G = (depthMap[:, :, 1]).astype(np.uint16) * 256
        depthMapDecoded = ((R + G) / (2 ** 16 - 1)) * maxDepth

    elif decodeDepthMapRange == "24-bit":
        # Decode 24-bit depth map
        depthMap = depthMap[:, :, :3]
        depthMap = depthMap[:, :, ::-1]
        # Decode 24-bit depth map
        R = (depthMap[:, :, 0]).astype(np.uint32)
        G = (depthMap[:, :, 1]).astype(np.uint32) * 256
        B = (depthMap[:, :, 2]).astype(np.uint32) * 256 ** 2

        depthMapDecoded = ((R + G + B) / (2 ** 24 - 1)) * maxDepth

    if depthMapDecoded is None:
        raise RuntimeError(Fore.RED + "\nDepth map decoding failed!\n")

    else:
        print(Fore.GREEN + f"\nDepth map successfully decoded ({decodeDepthMapRange})")

    return depthMapDecoded