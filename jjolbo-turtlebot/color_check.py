# Detecting traffic light using HoughCircles - red, yellow, green
import cv2
import numpy as np

cap = cv2.VideoCapture(2)
CIRCLE_SIZE = 3000

while True:

    # covert video frame to HSV
    _, frame = cap.read()

    # bluring for eliminate noises
    img = frame.copy()

    M = np.ones(img.shape, dtype="uint8") * 50
    img = cv2.subtract(img, M)
    # cv2.imshow('d', subtracted)

    img = cv2.medianBlur(img, 5)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of color in HSV
    # lowerYellow = np.array([20, 90, 100])
    # upperYellow = np.array([32, 255, 255])
    # lowerGreen = np.array([45, 100, 100])
    # upperGreen = np.array([93, 255, 210])
    # lowerRed = np.array([140, 100, 100])
    # upperRed = np.array([180, 255, 255])
    #
    # # sensitivity = 20
    # lowerWhite = np.array([0, 0, 150])
    # upperWhite = np.array([255, 50, 255])

    # from robotis's code
    #
    # lowerRed = np.array([-10, 150, 38])
    # upperRed = np.array([10, 255, 255])
    lowerYellow = np.array([20, 100, 50])
    upperYellow = np.array([35, 255, 255])
    # lowerGreen = np.array([46, 86, 50])
    # upperGreen = np.array([76, 255, 255])
    #

    # Threshold the HSV image to get three of colors
    # maskR = cv2.inRange(hsv, lowerRed, upperRed)
    maskY = cv2.inRange(hsv, lowerYellow, upperYellow)
    # maskG = cv2.inRange(hsv, lowerGreen, upperGreen)
    # maskW = cv2.inRange(hsv, lowerWhite, upperWhite)

    resY = cv2.bitwise_and(img, img, mask=maskY)
    # resG = cv2.bitwise_and(frame, frame, mask=maskG)
    # resR = cv2.bitwise_and(frame, frame, mask=maskR)
    # resW = cv2.bitwise_and(frame, frame, mask=maskW)

    traffic_stat = ""


    print(traffic_stat)

    cv2.imshow('img', img)
    cv2.imshow('white', resY)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
