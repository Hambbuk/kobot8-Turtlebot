# use houghlineP function
# detect line in gray scale

import numpy as np
import cv2

video = cv2.VideoCapture(2)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:

    ret, frame = video.read()   #normally read frame? True: False

    line_img = frame.copy()

    edges = cv2.Canny(frame, 50, 200, apertureSize=3)
    blured = cv2.GaussianBlur(edges, (3, 3), 0)
    gray = cv2.cvtColor(blured, cv2.COLOR_GRAY2BGR)
    minLineLength = 50
    maxLineGap = 30

    lines = cv2.HoughLinesP(blured, 1, np.pi / 360, 100, minLineLength, maxLineGap)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 5)

    src = np.array([[0, 200], [480, 200], [480, 360], [0, 360]], np.float32)
    dst = np.array([[0, 0], [480, 0], [300, 360], [180, 360]], np.float32)

    M = cv2.getPerspectiveTransform(src, dst)
    warp = cv2.warpPerspective(frame, M, (480, 360))
    cv2.imshow('transform', warp)
    cv2.imshow("line image", line_img)
    cv2.imshow("edges", edges)
    cv2.imshow("blured", blured)
    cv2.imshow("image", frame)


    if cv2.waitKey(1) > 0: break

video.release()
cv2.destroyAllWindows()
