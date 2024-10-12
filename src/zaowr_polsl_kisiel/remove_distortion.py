import cv2 as cv


def remove_distortion(
    cameraMatrix: Any,
    distortionCoefficients: Any,
    imgToUndistortPath: str,
    showImgToUndistort: bool = False,
    showUndistortedImg: bool = False,
    saveUndistortedImg: bool = False,
    undistortedImgPath: str = "",
    undistortionMethod: str = "undistort",
) -> None:

    if (imgToUndistortPath == "") or (not isinstance(imgToUndistortPath, str)):
        raise imgToUndistortPathNotProvided(
            "Path to the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program."
        )

    if saveUndistortedImg and (
        (undistortedImgPath == "") or (not isinstance(undistortedImgPath, str))
    ):
        raise undistortedImgPathNotProvided(
            "Path to save the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program."
        )

    # "../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/58.png"
    img = cv.imread(imgToUndistortPath)

    if showImgToUndistort:
        cv.imshow("Current Image", img)
        print("\nPress any key to continue...")
        cv.waitKey()

    h, w = img.shape[:2]
    newOptimalCameraMatrix, roi = cv.getOptimalNewCameraMatrix(
        cameraMatrix, distortionCoefficients, (w, h), 0.3, (w, h)
    )

    if undistortionMethod == "undistort":
        dst = cv.undistort(
            img, cameraMatrix, distortionCoefficients, None, newOptimalCameraMatrix
        )

        # crop the image
        x, y, w, h = roi
        dst = dst[y : y + h, x : x + w]

        if showUndistortedImg:
            cv.imshow(dst)
            print("\nPress any key to continue...")
            cv.waitKey()

        if saveUndistortedImg:
            cv.imwrite(undistortedImgPath, dst)

    elif undistortionMethod == "remapping":
        mapx, mapy = cv.initUndistortRectifyMap(
            cameraMatrix,
            distortionCoefficients,
            None,
            newOptimalCameraMatrix,
            (w, h),
            5,
        )
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

        # crop the image
        x, y, w, h = roi
        dst = dst[y : y + h, x : x + w]

        if showUndistortedImg:
            cv.imshow(dst)
            print("\nPress any key to continue...")
            cv.waitKey()

        if saveUndistortedImg:
            cv.imwrite(undistortedImgPath, dst)
