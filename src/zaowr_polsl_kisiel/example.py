import numpy as np
import cv2 as cv
import glob
import json




    # undistortion(mtx, dist, type="undistort")
    # undistortion(mtx, dist, type="remapping")





if __name__ == "__main__":
    try:
        # main()
        dump = read_calibration()
        # corners = dump["corners1"]
        # corners2 = dump["corners2"]
        mean_error = dump["mean_error"]
        ret = dump["ret"]
        mtx = np.array(dump["mtx"])
        dist = np.array(dump["dist"])
        rvecs = dump["rvecs"]
        tvecs = dump["tvecs"]

        undistortion(
            mtx,
            dist,
            "../img/undistort_calibresult_2.png",
            type="undistort",
        )
        undistortion(
            mtx,
            dist,
            "../img/remapping_calibresult_2.png",
            type="remapping",
        )

    except Exception as e:
        print(e)
    finally:
        cv.destroyAllWindows()
        print("done")
