import cv2
import numpy as np

cap = cv2.VideoCapture(2)
CIRCLE_SIZE = 3000

while True:

    # covert video frame to HSV image
    _, frame = cap.read()

    #bluring for eliminate noises
    img = cv2.medianBlur(frame, 5)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of color in HSV
    lowerYellow = np.array([15, 90, 100])
    upperYellow = np.array([30, 255, 255])
    lowerGreen = np.array([55, 100, 100])
    upperGreen = np.array([80, 255, 255])
    lowerRed = np.array([-15, 180, 100])
    upperRed = np.array([10, 255, 255])



    # Threshold the HSV image to get three of colors
    maskY = cv2.inRange(hsv, lowerYellow, upperYellow)
    maskG = cv2.inRange(hsv, lowerGreen, upperGreen)
    maskR = cv2.inRange(hsv, lowerRed, upperRed)
    # Bitwise-AND mask and original image


    circle = frame.copy()

    contours, _ = cv2.findContours(maskR, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > CIRCLE_SIZE:                 # please change area size to fit in traffic light size
            cv2.drawContours(circle, contours, -1, (0,255,0), 3)
            print(area)



    contours, _ = cv2.findContours(maskG, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > CIRCLE_SIZE:  # please change area size to fit in traffic light size
            cv2.drawContours(circle, contours, -1, (0, 255, 0), 3)

    contours, _ = cv2.findContours(maskY, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > CIRCLE_SIZE:  # please change area size to fit in traffic light size
            cv2.drawContours(circle, contours, -1, (0, 255, 0), 3)


    cv2.imshow('dst', circle)
    # print('area=', area)
    print('len(contours)=', len(contours))


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

    cv2.imshow('Yellow',resY)
    cv2.imshow('green', resG)
    cv2.imshow('Red', resR)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
