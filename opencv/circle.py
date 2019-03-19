import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:

    # covert video frame to HSV image
    _, frame = cap.read()

    #bluring for eliminate noises
    img = cv2.medianBlur(frame, 5)


    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of color in BGR
    lowerYellow = np.array([15, 100, 100])
    upperYellow = np.array([30, 255, 255])
    lowerGreen = np.array([45, 80, 80])
    upperGreen = np.array([70, 255, 255])
    lowerRed = np.array([-10, 150, 150])
    upperRed = np.array([10, 255, 255])



    # Threshold the HSV image to get three of colors
    maskY = cv2.inRange(hsv, lowerYellow, upperYellow)
    maskG = cv2.inRange(hsv, lowerGreen, upperGreen)
    maskR = cv2.inRange(hsv, lowerRed, upperRed)
    # Bitwise-AND mask and original image
    resY = cv2.bitwise_and(frame, frame, mask=maskY)
    resG = cv2.bitwise_and(frame, frame, mask=maskG)
    resR = cv2.bitwise_and(frame, frame, mask=maskR)


    if maskY.any():
        print("yellow")
    if maskG.any():
        print("green")
    if maskR.any():
        print("red")

    cv2.imshow('frame',frame)
    cv2.imshow('hsv', hsv)
    cv2.imshow('maskR',maskR)
    cv2.imshow('Yellow',resY)
    cv2.imshow('green', resG)
    cv2.imshow('Red', resR)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
