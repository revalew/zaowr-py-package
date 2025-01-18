import os

import cv2 as cv
import numpy as np
from colorama import Fore, init as colorama_init

from . import read_images_from_folder

colorama_init(autoreset=True)

def dense_optical_flow(
        source: str | int = -1,  # -1 for 1st accessible webcam
        pyr_scale: float = 0.5,
        levels: int = 3,
        winsize: int = 15,
        iterations: int = 3,
        poly_n: int = 5,
        poly_sigma: float = 1.2,
        flags: int = 0,
        windowSize: tuple[int, int] = (1080, 720),
        windowName: str = "Dense optical flow",
) -> None:
    """
    Calculate dense optical flow using Farneback's algorithm

    :param source: The source of the video feed. Can be a camera number, video file path, or folder with images.
    :param pyr_scale: The pyramid scale factor for Farneback's algorithm.
    :param levels: The number of pyramid levels for Farneback's algorithm.
    :param winsize: The window size for Farneback's algorithm.
    :param iterations: The number of iterations for Farneback's algorithm.
    :param poly_n: The polynomial order for Farneback's algorithm.
    :param poly_sigma: The standard deviation for Farneback's algorithm.
    :param flags: The flags for Farneback's algorithm.
    :param windowSize: The size of the window to display the optical flow.
    :param windowName: The name of the window to display the optical flow.

    :raises ValueError: Raises ValueError if:
        - **`source`** is None.
        - **`source`** is **NOT** an integer, a string, or a folder path.

    :raises IOError: Raises IOError if:
        - **`source`** is a video file path and the file could not be loaded.

    :return: None
    """

    # Determine the type of source
    if source is None:
        raise ValueError(Fore.RED + f"\nInvalid source! Provide a camera number, video file path, or folder with images ('{source}' provided)\n\n")

    elif isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
        # Case: Camera feed (number)
        # The video feed is read in as a VideoCapture object
        cap = cv.VideoCapture(int(source))
        sourceType = "camera"

    elif os.path.isdir(source):
        # Case: Folder with images
        imagePaths = read_images_from_folder(source)
        cap = None
        sourceType = "images"

    elif os.path.isfile(source):
        # Case: Video file
        # The video feed is read in as a VideoCapture object
        cap = cv.VideoCapture(source)
        sourceType = "video"

    else:
        raise ValueError(Fore.RED + f"\nInvalid source! Provide a camera number, video file path, or folder with images ('{source}' provided)\n\n")

    # Parameters for Farneback optical flow
    fbParams = dict(
        pyr_scale=pyr_scale,
        levels=levels,
        winsize=winsize,
        iterations=iterations,
        poly_n=poly_n,
        poly_sigma=poly_sigma,
        flags=flags
    )

    # Initialization for different source types
    if sourceType == "images":
        oldFrame = cv.imread(imagePaths[0])
        imageIter = iter(imagePaths[1:])

    else:
        # Take first frame and find corners in it
        # ret = a boolean return value from getting the frame, oldFrame = the first frame in the entire video sequence
        ret, oldFrame = cap.read()

        if not ret:
            raise IOError(Fore.RED + f"\nUnable to read source: {source}\n")

    oldGray = cv.cvtColor(oldFrame, cv.COLOR_BGR2GRAY)
    mask = np.zeros_like(oldFrame) # HSV mask
    mask[..., 1] = 255 # Sets image saturation to maximum

    print(Fore.GREEN + f"\nReading from source (type: '{sourceType}'): {source}")
    # print(Fore.GREEN + f"\nWindow '{windowName}' is going to be moved to the edge of the screen - (0, 0)...")
    print(Fore.GREEN + "\nPress `Esc` or `q` to exit...\nPress `s` to save current frame...")

    frameCount = 0
    while True:
        # Read next frame or image
        if sourceType == "images":
            try:
                framePath = next(imageIter)
                frame = cv.imread(framePath)

            except StopIteration:
                print(Fore.YELLOW + "\nEnd of images in folder.")
                print(Fore.YELLOW + "Press any key to exit...")
                cv.waitKey(0)
                break

        else:
            # ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
            ret, frame = cap.read()

            if not ret:
                print(Fore.YELLOW + "\nNo more frames to read.")
                print(Fore.YELLOW + "Press any key to exit...")
                cv.waitKey(0)
                break

        # Convert frame to grayscale for easier calculations
        frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Calculates dense optical flow by Farneback method
        # https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowfarneback
        # flow = cv.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        flow = cv.calcOpticalFlowFarneback(oldGray, frameGray, None, **fbParams)

        # Computes the magnitude and angle of the 2D vectors
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        # Sets image hue according to the optical flow direction
        mask[..., 0] = ang * 180 / np.pi / 2
        # Sets image value according to the optical flow magnitude (normalized)
        mask[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        # Converts HSV to RGB (BGR) color representation
        bgr = cv.cvtColor(mask, cv.COLOR_HSV2BGR)

        # Set window size and position for large images
        if bgr.shape[0] > windowSize[1] or bgr.shape[1] > windowSize[0]:
            cv.namedWindow(windowName, cv.WINDOW_NORMAL)
            cv.resizeWindow(windowName, windowSize)

        else:
            cv.namedWindow(windowName, cv.WINDOW_AUTOSIZE)

        # cv.moveWindow(windowName, 0, 0)

        # Break if window is closed
        if cv.getWindowProperty(windowName, cv.WND_PROP_VISIBLE) < 1:
            break

        cv.imshow(windowName, bgr)

        # Frames are read by intervals of 30 milliseconds. The programs breaks out of the while loop when the user presses the 'Esc' or 'q' key
        # if 's' is pressed, it saves the current frame
        k = cv.waitKey(30) & 0xff
        if k == 27 or k == ord('q'):
            break

        elif k == ord('s'):
            denseDir = "dense_flow"
            if not os.path.exists(denseDir):
                os.makedirs(denseDir)

            cv.imwrite(os.path.join(denseDir, f'dense_original_{frameCount}.png'), frame)
            cv.imwrite(os.path.join(denseDir, f'dense_mask_{frameCount}.png'), bgr)

            print(Fore.GREEN + f"\nDense flow frame no. {frameCount} saved to folder: {denseDir}")

        oldGray = frameGray.copy()
        frameCount += 1

    # Release resources and close windows
    if cap is not None:
        cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    # Provide the source: camera number, video path, or folder path
    videoPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/optical_flow/slow_traffic_small.mp4"

    # videoPath = None
    # videoPath = 2
    # videoPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam1/"

    dense_optical_flow(
        source=videoPath,
    )