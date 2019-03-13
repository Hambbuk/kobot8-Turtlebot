# detect only yellow line

import cv2
import numpy as np

video = cv2.VideoCapture(2)

while True:
    ret, orig_frame = video.read()
    if not ret:
        video = cv2.VideoCapture(0)
        continue

    draw_temp = orig_frame.copy()

    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    low_yellow = np.array([18, 94, 140])
    up_yellow = np.array([48, 255, 255])
    mask = cv2.inRange(hsv, low_yellow, up_yellow)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    cv2.imshow("aa", mask)

    edges = cv2.Canny(mask, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 3)

    if lines is not None:
        for rho, theta in lines[0]:
            print(rho,'\n', theta)
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

        cv2.line(draw_temp, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv2.imshow('edges', draw_temp)


    # lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)
    # if lines is not None:
    #     for line in lines:
    #         x1, y1, x2, y2 = line[0]
    #         cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    #
    # cv2.imshow("frame", frame)
    # cv2.imshow("edges", edges)

    key = cv2.waitKey(25)
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()
