import cv2
import numpy as np


cap = cv2.VideoCapture(0)
CIRCLE_SIZE = 3000

while True:

    # covert video frame to HSV
    _, frame = cap.read()

    #bluring for eliminate noises
    img = frame.copy()

    img = cv2.medianBlur(img, 5)


    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of color in HSV
    lowerYellow = np.array([20, 90, 100])
    upperYellow = np.array([32, 255, 255])
    lowerGreen = np.array([45, 70, 80])
    upperGreen = np.array([95, 255, 255])
    lowerRed = np.array([140, 100, 100])
    upperRed = np.array([180, 255, 255])

    #from robotis's code
    #
    # lowerRed = np.array([-10, 150, 38])
    # upperRed = np.array([10, 255, 255])
    # lowerYellow = np.array([20, 100, 50])
    # upperYellow = np.array([35, 255, 255])
    # lowerGreen = np.array([46, 86, 50])
    # upperGreen = np.array([76, 255, 255])
    #


    # Threshold the HSV image to get three of colors
    maskR = cv2.inRange(hsv, lowerRed, upperRed)
    maskY = cv2.inRange(hsv, lowerYellow, upperYellow)
    maskG = cv2.inRange(hsv, lowerGreen, upperGreen)




    resY = cv2.bitwise_and(frame, frame, mask=maskY)
    resG = cv2.bitwise_and(frame, frame, mask=maskG)
    resR = cv2.bitwise_and(frame, frame, mask=maskR)

    traffic_stat=0

    if maskY.any():
        print("yellow")
        # cimg = cv2.cvtColor(maskY, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(maskY, cv2.HOUGH_GRADIENT, 4, 20,
                                   param1=100, param2=100, minRadius=0, maxRadius=0)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)

            traffic_stat = 1

    if maskG.any():
        print("green")
        # cimg = cv2.cvtColor(maskY, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(maskG, cv2.HOUGH_GRADIENT, 4, 20,
                                   param1=100, param2=100, minRadius=0, maxRadius=0)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)

            traffic_stat = 2

    if maskR.any():
        print("red")
        # cimg = cv2.cvtColor(maskY, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(maskR, cv2.HOUGH_GRADIENT, 4, 20,
                                   param1=100, param2=100, minRadius=0, maxRadius=0)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)

            traffic_stat = 3

    print(traffic_stat)

    cv2.imshow('img',img)

    cv2.imshow('Yellow',resY)
    cv2.imshow('green', resG)
    cv2.imshow('Red', resR)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
