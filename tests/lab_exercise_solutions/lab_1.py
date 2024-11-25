import zaowr_polsl_kisiel as zw

calibrationFile = "./calibration_params.json"
calibrationFileNoSubPix = "./calibration_params_no_subpix.json"


zw.calibrate_camera(
    chessBoardSize=(10, 7),
    squareRealDimensions=28.67,
    calibImgDirPath="../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/",
    saveCalibrationParams=True,
    calibrationParamsPath=calibrationFileNoSubPix,
    displayFoundCorners=False,
    improveSubPix=False,
)


zw.calibrate_camera(
    chessBoardSize=(10, 7),
    squareRealDimensions=28.67,
    calibImgDirPath="../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/",
    saveCalibrationParams=True,
    calibrationParamsPath=calibrationFile,
    displayFoundCorners=False,
)

imgToUndistort = "../img/distorted.png"

calibrationParams1 = zw.load_calibration(calibrationFile)
cameraMatrix1 = calibrationParams1["cameraMatrix"]
distortionCoef1 = calibrationParams1["distortionCoefficients"]

calibrationParams2 = zw.load_calibration(calibrationFileNoSubPix)
cameraMatrix2 = calibrationParams2["cameraMatrix"]
distortionCoef2 = calibrationParams2["distortionCoefficients"]

zw.remove_distortion(
    cameraMatrix=cameraMatrix1,
    distortionCoefficients=distortionCoef1,
    imgToUndistortPath=imgToUndistort,
    showUndistortedImg=True,
)

zw.remove_distortion(
    cameraMatrix=cameraMatrix2,
    distortionCoefficients=distortionCoef2,
    imgToUndistortPath=imgToUndistort,
    showUndistortedImg=True,
)
