import zaowr_polsl_kisiel as zw


def main():
    # https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4
    # Provide the source: camera number, video path, or folder path
    videoPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/optical_flow/slow_traffic_small.mp4"

    # videoPath = None
    # videoPath = 2
    # videoPath = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam1/"

    ###############################
    # EX 1 (sparse_optical_flow)
    ###############################
    zw.sparse_optical_flow(
        source=videoPath,
    )

    ###############################
    # EX 2 (dense_optical_flow)
    ###############################
    zw.dense_optical_flow(
        source=videoPath,
    )

    ###############################
    # EX 3 (sparse_optical_flow)
    ###############################
    zw.sparse_optical_flow(
        source=videoPath,
        maxCorners=300,
        qualityLevel=0.1,
        minDistance=7,
        blockSize=5,
        winSize=(15, 15),
        maxLevel=2,
        drawBboxes=True,
    )

    ###############################
    # EX 3 (dense_optical_flow)
    ###############################
    zw.dense_optical_flow(
        source=videoPath,
        levels=3,
        winsize=11,
        iterations=4,
        drawBboxes=True,
        scaleFactor=.6,
        clusteringMethod="l1",
        clusteringEps=15,  # Promień dla klasteryzacji
        minClusterSize=100,  # Minimalna liczba pikseli w klastrze
    )

    ###############################
    # EX 4 (sparse_optical_flow)
    ###############################
    zw.sparse_optical_flow(
        source=videoPath,
        maxCorners=300,
        qualityLevel=0.1,
        minDistance=7,
        blockSize=5,
        winSize=(15, 15),
        maxLevel=2,
        drawBboxes=True,
        speedFilter=2,  # Minimalna prędkość ruchu
        directionFilter=(-45, 45)  # Reaguje tylko na ruch w poziomie
    )

    ###############################
    # EX 4 (dense_optical_flow)
    ###############################
    zw.dense_optical_flow(
        source=videoPath,
        levels=2,
        winsize=9,
        iterations=2,
        drawBboxes=True,
        scaleFactor=.5,
        speedFilter=2,  # Minimalna prędkość
        directionFilter=(45, 135),  # Ruch w zakresie 45° - 135°
        clusteringMethod="euclidean",
        clusteringEps=20,  # Promień dla klasteryzacji
        minClusterSize=50,  # Minimalna liczba pikseli w klastrze
    )

if __name__ == '__main__':
    main()