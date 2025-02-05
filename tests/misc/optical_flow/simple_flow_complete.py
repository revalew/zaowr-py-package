import cv2 as cv
import numpy as np
import time


def sparse_optical_flow(video_path):
    cap = cv.VideoCapture(video_path)
    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
    lk_params = dict(winSize=(15, 15), maxLevel=2,
                     criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
    color = np.random.randint(0, 255, (100, 3))

    ret, old_frame = cap.read()
    old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
    p0 = cv.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
    mask = np.zeros_like(old_frame)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
            frame = cv.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)

        img = cv.add(frame, mask)
        cv.imshow('Sparse Optical Flow', img)

        if cv.waitKey(30) & 0xFF == 27:
            break

        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)

    cap.release()
    cv.destroyAllWindows()


def dense_optical_flow(video_path):
    cap = cv.VideoCapture(video_path)
    ret, frame1 = cap.read()
    prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255

    while cap.isOpened():
        ret, frame2 = cap.read()
        if not ret:
            break

        next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

        cv.imshow('Dense Optical Flow', bgr)

        if cv.waitKey(30) & 0xFF == 27:
            break

        prvs = next

    cap.release()
    cv.destroyAllWindows()


def moving_objects_detection(video_path):
    cap = cv.VideoCapture(video_path)
    ret, frame1 = cap.read()
    prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)

    while cap.isOpened():
        ret, frame2 = cap.read()
        if not ret:
            break

        next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        motion_magnitude = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        _, motion_mask = cv.threshold(motion_magnitude, 15, 255, cv.THRESH_BINARY)
        motion_mask = motion_mask.astype(np.uint8)

        contours, _ = cv.findContours(motion_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv.contourArea(cnt) > 500:
                x, y, w, h = cv.boundingRect(cnt)
                cv.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv.imshow('Motion Detection', frame2)

        if cv.waitKey(30) & 0xFF == 27:
            break

        prvs = next

    cap.release()
    cv.destroyAllWindows()


def real_time_analysis(source=-1):
    cap = cv.VideoCapture(source)
    ret, frame1 = cap.read()
    prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    start_time = time.time()
    frame_count = 0

    while cap.isOpened():
        ret, frame2 = cap.read()
        if not ret:
            break

        next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        motion_magnitude = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        _, motion_mask = cv.threshold(motion_magnitude, 15, 255, cv.THRESH_BINARY)
        motion_mask = motion_mask.astype(np.uint8)

        contours, _ = cv.findContours(motion_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv.contourArea(cnt) > 500:
                x, y, w, h = cv.boundingRect(cnt)

                # Calculate average speed and direction
                avgSpeed = cnt.mean()
                avgAngle = np.degrees(cnt.mean())

                # Draw green bounding box around the cluster
                cv.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Add speed and direction text
                txtColor = (0, 255, 0)
                speedText = f"Speed: {avgSpeed:.2f} px/frame"
                directionText = f"Dir: {avgAngle:.1f} deg"
                cv.putText(frame2, speedText, (x, y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, txtColor, 1)
                cv.putText(frame2, directionText, (x, y - 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, txtColor, 1)

        cv.imshow('Real-Time Analysis', frame2)

        if cv.waitKey(30) & 0xFF == 27:
            break

        prvs = next
        frame_count += 1

    elapsed_time = time.time() - start_time
    print(f'Average processing time per frame: {elapsed_time / frame_count:.2f} seconds')

    cap.release()
    cv.destroyAllWindows()


# Example Usage
# Replace 'video_path' with the path to your video file or use 0 for real-time capture.
video_path = 'vtest.avi'
video_path = "/run/media/maks/Dokumenty 2/Studia/Infa Magister/Infa sem 2/ZAOWR Zaawansowana Analiza Obrazu, Wideo i Ruchu/zaowr_py_package/tests/misc/optical_flow/slow_traffic_small.mp4"
# sparse_optical_flow(video_path)
# dense_optical_flow(video_path)
# moving_objects_detection(video_path)
real_time_analysis(2)
