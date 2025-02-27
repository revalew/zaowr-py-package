import os

import cv2 as cv
import numpy as np
from colorama import Fore, init as colorama_init
from sklearn.cluster import DBSCAN

# from . import read_images_from_folder
from read_images_from_folder import read_images_from_folder

colorama_init(autoreset=True)

def cluster_and_draw_boxes(
        frame: np.ndarray,
        pointsOld: np.ndarray,
        pointsNew: np.ndarray,
        eps: float = 50,
        minSamples: int = 2,
        movementThreshold: float = 1,
        smoothing_factor: float = 0.5,  # Stabilizacja bounding-boxów
        prev_boxes: list = None  # Przechowywanie poprzednich pozycji boxów
) -> np.ndarray:
    """
    Cluster moving points and draw separate bounding boxes for each cluster.

    :param frame: Current video frame.
    :param pointsOld: Points from the previous frame.
    :param pointsNew: Points from the current frame.
    :param eps: Maximum distance between two points to be in the same cluster.
    :param minSamples: Minimum number of points in a cluster.
    :param float movementThreshold: Threshold for determining if an object is moving.
    :param smoothing_factor: Factor for smoothing bounding-box positions.
    :param prev_boxes: Previous bounding boxes for smoothing.

    :return: Frame with bounding boxes.
    """
    # Calculate motion vectors
    motion_vectors = pointsNew - pointsOld
    magnitudes = np.linalg.norm(motion_vectors, axis=1)

    # Filter points with significant movement
    moving_points = pointsNew[magnitudes > movementThreshold]
    moving_vectors = motion_vectors[magnitudes > movementThreshold]  # Filter corresponding motion vectors

    if len(moving_points) > 0:
        # Clustering using DBSCAN
        clustering = DBSCAN(eps=eps, min_samples=minSamples).fit(moving_points)
        labels = clustering.labels_

        new_boxes = []
        for label in set(labels):
            if label == -1:  # Ignore noise points
                continue

            # Select points in the current cluster
            cluster_points = moving_points[labels == label]
            cluster_motion = moving_vectors[labels == label]

            # Calculate bounding box for the cluster
            x_min, y_min = np.min(cluster_points, axis=0).astype(int)
            x_max, y_max = np.max(cluster_points, axis=0).astype(int)

            # Stabilize bounding boxes with smoothing
            if prev_boxes and len(prev_boxes) > label:
                prev_box = prev_boxes[label]
                x_min = int(smoothing_factor * prev_box[0] + (1 - smoothing_factor) * x_min)
                y_min = int(smoothing_factor * prev_box[1] + (1 - smoothing_factor) * y_min)
                x_max = int(smoothing_factor * prev_box[2] + (1 - smoothing_factor) * x_max)
                y_max = int(smoothing_factor * prev_box[3] + (1 - smoothing_factor) * y_max)

            # Save current box for the next frame
            new_boxes.append((x_min, y_min, x_max, y_max))

            # Draw the bounding box
            cv.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Calculate direction and speed
            avg_vector = np.mean(cluster_motion, axis=0)
            speed = np.linalg.norm(avg_vector)
            direction = np.arctan2(avg_vector[1], avg_vector[0]) * 180 / np.pi

            # Display speed and direction on the frame
            label_text = f"Speed: {speed:.2f}, Dir: {direction:.1f}°"
            cv.putText(frame, label_text, (x_min, y_min - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Update previous boxes
        return frame, new_boxes

    return frame, prev_boxes or []

def draw_bounding_boxes(
        frame: np.ndarray,
        pointsOld: np.ndarray,
        pointsNew: np.ndarray,
        movementThreshold: float = 1,
) -> np.ndarray:
    """
    Draw bounding boxes around moving objects based on optical flow points.

    :param np.ndarray frame: Current video frame.
    :param np.ndarray pointsOld: Previous frame points.
    :param np.ndarray pointsNew: Current frame points.
    :param float movementThreshold: Threshold for determining if an object is moving.

    :return: Frame with bounding boxes.
    """
    # Calculate motion vectors
    motionVectors = pointsNew - pointsOld

    # Determine if motion is significant
    magnitudes = np.linalg.norm(motionVectors, axis=1)
    threshold = movementThreshold  # Minimum motion to consider as movement
    movingPoints = pointsNew[magnitudes > threshold]

    if len(movingPoints) > 0:
        # Calculate bounding box around moving points
        xMin, yMin = np.min(movingPoints, axis=0).astype(int)
        xMax, yMax = np.max(movingPoints, axis=0).astype(int)

        # Draw the bounding box
        cv.rectangle(frame, (xMin, yMin), (xMax, yMax), (0, 255, 0), 2)

    return frame

def sparse_optical_flow(
        source: str | int = -1,  # -1 for 1st accessible webcam
        maxCorners: int = 100,
        qualityLevel: float = 0.3,
        minDistance: int = 7,
        blockSize: int = 7,
        winSize: tuple[int, int] = (15, 15),
        maxLevel: int = 2,
        criteria: tuple[int, int, float] = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03),
        drawBboxes: bool = False,
        movementThreshold: float = 2,
        windowSize: tuple[int, int] = (1080, 720),
        windowName: str = "Sparse optical flow",
) -> None:
    """
    Calculate sparse optical flow using Shi-Tomasi corner detection and Lucas-Kanade optical flow.

    :param source: The source of the video feed. Can be a camera number, video file path, or folder with images.
    :param maxCorners: The maximum number of corners to detect (**Shi-Tomasi**).
    :param qualityLevel: The quality level for corner detection (**Shi-Tomasi**).
    :param minDistance: The minimum distance between corners (**Shi-Tomasi**).
    :param blockSize: The block size for corner detection (**Shi-Tomasi**).
    :param winSize: The window size for Lucas-Kanade optical flow.
    :param maxLevel: The maximum pyramid level for Lucas-Kanade optical flow.
    :param criteria: The termination criteria for Lucas-Kanade optical flow.

    :param drawBboxes: If True, draws bounding boxes around moving objects.
    :param movementThreshold: Threshold for determining if an object is moving.

    :param windowSize: The size of the window to display the optical flow.
    :param windowName: The name of the window to display the optical flow.

    :raises ValueError: Raises ValueError if:
        - **`source`** is not an integer, a string, or a folder path.
        - **`maxCorners`** is not an integer.
        - **`qualityLevel`** is not a float.
        - **`minDistance`** is not an integer.
        - **`blockSize`** is not an integer.
        - **`winSize`** is not a tuple of two integers.
        - **`maxLevel`** is not an integer.
        - **`criteria`** is not a tuple of three integers.
        - **`windowSize`** is not a tuple of two integers.
        - **`windowName`** is not a string.

    :raises IOError: Raises IOError if:
        - **`source`** is a video file path and the file could not be loaded.

    :return: None
    """
    # Determine the type of source
    if isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
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
        raise ValueError(Fore.RED + f"\nInvalid source! Provide a camera number, video file path, or folder with images ({source})\n\n")

    # Parameters for Shi-Tomasi corner detection
    featureParams = dict(
        maxCorners=maxCorners,
        qualityLevel=qualityLevel,
        minDistance=minDistance,
        blockSize=blockSize
    )

    # Parameters for Lucas-Kanade optical flow
    lkParams = dict(
        winSize=winSize,
        maxLevel=maxLevel,
        criteria=criteria
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

    # Variable for color to draw optical flow track
    # color = (127, 127, 127)
    color = np.random.randint(0, 255, (oldGray.shape[0], 3))

    # Detect initial feature points
    p0 = cv.goodFeaturesToTrack(oldGray, mask=None, **featureParams)

    # Creates an image filled with zero intensities with the same dimensions as the frame - for later drawing purposes
    mask = np.zeros_like(oldFrame)

    print(Fore.GREEN + f"\nReading from source (type: '{sourceType}'): {source}")
    # print(Fore.GREEN + f"\nWindow '{windowName}' is going to be moved to the edge of the screen - (0, 0)...")
    print(Fore.GREEN + "\nPress `Esc` or `q` to exit...\nPress `s` to save current frame...")

    frameCount = 0
    goodOld, goodNew = None, None
    prev_boxes = []  # Initialize storage for previous boxes
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

        # Calculates sparse optical flow by Lucas-Kanade method
        # https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowpyrlk
        # next, status, error = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)
        p1, st, err = cv.calcOpticalFlowPyrLK(oldGray, frameGray, p0, None, **lkParams)

        # Select good points
        if p1 is not None:
            # Selects good feature points for previous position
            goodOld = p0[st == 1]
            # Selects good feature points for next position
            goodNew = p1[st == 1]

        if goodOld is None or goodNew is None:
            continue

        # draw the tracks
        for i, (new, old) in enumerate(zip(goodNew, goodOld)):
            # Returns a contiguous flattened array as (x, y) coordinates for new point
            a, b = new.ravel()
            # Returns a contiguous flattened array as (x, y) coordinates for old point
            c, d = old.ravel()
            # Draws line between new and old position with green color and 2 thickness
            mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
            # mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)), color, 2)
            # Draws filled circle (thickness of -1) at new position with green color and radius of 3
            frame = cv.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)
            # frame = cv.circle(frame, (int(a), int(b)), 5, color, -1)


        # Draw bounding boxes around moving objects
        if drawBboxes:
            # frame2 = draw_bounding_boxes(frame, goodOld, goodNew)
            # frame = cv.add(frame, frame2)
            # frame = draw_bounding_boxes(frame, goodOld, goodNew, movementThreshold)
            # frame = cluster_and_draw_boxes(frame, goodOld, goodNew, 200, 4, movementThreshold)
            # Cluster points and draw bounding boxes with stabilization
            frame, prev_boxes = cluster_and_draw_boxes(frame, goodOld, goodNew, 50, 2, movementThreshold, prev_boxes=prev_boxes)

        # Overlays the optical flow tracks on the original frame
        img = cv.add(frame, mask)

        # print(f"{img.shape[0] = ^24}")
        # print(f"{img.shape[1] = ^24}")
        # print(f"{windowSize[0] = ^24}")
        # print(f"{windowSize[1] = ^24}")

        # Set window size and position for large images
        if img.shape[0] > windowSize[1] or img.shape[1] > windowSize[0]:
            cv.namedWindow(windowName, cv.WINDOW_NORMAL)
            cv.resizeWindow(windowName, windowSize)

        else:
            cv.namedWindow(windowName, cv.WINDOW_AUTOSIZE)

        # cv.moveWindow(windowName, 0, 0)

        # Break if window is closed
        if cv.getWindowProperty(windowName, cv.WND_PROP_VISIBLE) < 1:
            break

        cv.imshow(windowName, img)

        # Frames are read by intervals of 30 milliseconds. The programs breaks out of the while loop when the user presses the 'Esc' or 'q' key
        k = cv.waitKey(30) & 0xff
        if k == 27 or k == ord('q'):
            break

        elif k == ord('s'):
            sparseDir = "sparse_flow"
            if not os.path.exists(sparseDir):
                os.makedirs(sparseDir)

            cv.imwrite(os.path.join(sparseDir, f'sparse_original_{frameCount}.png'), frame)
            cv.imwrite(os.path.join(sparseDir, f'sparse_mask_{frameCount}.png'), img)

            print(Fore.GREEN + f"\nSparse flow frame no. {frameCount} saved to folder: {sparseDir}")

        # Now update the previous frame and previous points
        oldGray = frameGray.copy()
        p0 = goodNew.reshape(-1, 1, 2)

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

    sparse_optical_flow(
        source=videoPath,
        maxCorners = 300,
        qualityLevel = 0.2,
        minDistance = 2,
        blockSize = 7,
        winSize = (13, 13),
        maxLevel = 10,
        drawBboxes=True,
        movementThreshold = 1.1,
        # movementThreshold = .7,
    )
