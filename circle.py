import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:

    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of color in BGR
    lowerBlue = np.array([100, 80, 80])
    upperBlue = np.array([140, 255, 255])
    lowerGreen = np.array([35, 80, 80])
    upperGreen = np.array([80, 255, 255])
    lowerRed = np.array([-10, 100, 100])
    upperRed = np.array([10, 255, 255])

    # Threshold the HSV image to get three of colors
    maskB = cv2.inRange(hsv, lowerBlue, upperBlue)
    maskG = cv2.inRange(hsv, lowerGreen, upperGreen)
    maskR = cv2.inRange(hsv, lowerRed, upperRed)

    # Bitwise-AND mask and original image
    resB = cv2.bitwise_and(frame, frame, mask=maskB)
    resG = cv2.bitwise_and(frame, frame, mask=maskG)
    resR = cv2.bitwise_and(frame, frame, mask=maskR)

    cv2.imshow('frame',frame)
    cv2.imshow('maskR',maskR)
    cv2.imshow('blue',resB)
    cv2.imshow('green', resG)
    cv2.imshow('Red', resR)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()