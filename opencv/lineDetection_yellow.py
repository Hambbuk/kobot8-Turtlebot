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
    yellow_mask = cv2.inRange(hsv, low_yellow, up_yellow)
    yellow_mask = cv2.erode(yellow_mask, None, iterations=1)
    yellow_mask = cv2.dilate(yellow_mask, None, iterations=1)

    edges = cv2.Canny(yellow_mask, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 3)

    if lines is not None:
        for rho, theta in lines[0]:
            print('yellow-', 'rho: ', rho, '\t\ttheta: ' ,theta)
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

        cv2.line(draw_temp, (x1, y1), (x2, y2), (255, 0, 0), 2)

    sensitivity = 15
    lower_white = np.array([0, 0, 255 - sensitivity])
    upper_white = np.array([255, sensitivity, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    white_mask = cv2.erode(white_mask, None, iterations=1)
    white_mask = cv2.dilate(white_mask, None, iterations=1)

    edges = cv2.Canny(white_mask, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 3)

    if lines is not None:
        for rho, theta in lines[0]:
            print('white-', 'rho: ', rho, '\t\ttheta: ', theta)
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



    key = cv2.waitKey(25)
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()
