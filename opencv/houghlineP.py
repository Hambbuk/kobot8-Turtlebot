# use houghlineP function 
# detect line in gray scale

import numpy as np
import cv2

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:

    ret, frame = camera.read()

    edges = cv2.Canny(frame, 50, 200, apertureSize=3)
    gray = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    minLineLength = 50
    maxLineGap = 50

    lines = cv2.HoughLinesP(edges, 1, np.pi / 360, 100, minLineLength, maxLineGap)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(gray, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow("img3", gray)


    if cv2.waitKey(1) > 0: break

camera.release()
cv2.destroyAllWindows()

