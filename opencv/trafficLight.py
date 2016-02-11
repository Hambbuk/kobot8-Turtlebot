# Detecting traffic light using HoughCircles - red, yellow, green 
import cv2
import numpy as np


cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 360)
CIRCLE_SIZE = 3000

while True:
    # covert video frame to HSV
    _, frame = cap.read()

    draw_temp = frame.copy()

    M = np.ones(draw_temp.shape, dtype="uint8") * 10
    draw_temp = cv2.subtract(draw_temp, M)

    #bluring for eliminate noises

    img = cv2.medianBlur(draw_temp, 5)


    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of color in HSV
    #lowerYellow = np.array([20, 90, 100])
    #upperYellow = np.array([32, 255, 255])
    #lowerGreen = np.array([45, 100, 100])
    #upperGreen = np.array([93, 255, 210])
    lowerRed = np.array([140, 100, 100])
    upperRed = np.array([180, 255, 255])

    #from robotis's code
    #
    #lowerRed = np.array([-10, 150, 38])
    #upperRed = np.array([10, 255, 255])
    # lowerYellow = np.array([20, 100, 50])
    # upperYellow = np.array([35, 255, 255])
    lowerGreen = np.array([46, 86, 50])
    upperGreen = np.array([76, 255, 255])
    #


    # Threshold the HSV image to get three of colors
    maskR = cv2.inRange(hsv, lowerRed, upperRed)
    #maskY = cv2.inRange(hsv, lowerYellow, upperYellow)
    maskG = cv2.inRange(hsv, lowerGreen, upperGreen)

    #resY = cv2.bitwise_and(frame, frame, mask=maskY)
    resG = cv2.bitwise_and(draw_temp, draw_temp, mask=maskG)
    resR = cv2.bitwise_and(draw_temp, draw_temp, mask=maskR)

    traffic_stat=""
    
    #If yellow color detected, find circle from yellow mask image and show 'yellow' text

            
    #If green color detected, find circle from green mask image and show 'green' text
    if maskG.any():
        circles = cv2.HoughCircles(maskG, cv2.HOUGH_GRADIENT, 4, 20,
                                   param1=100, param2=100, minRadius=0, maxRadius=0)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # put text in detected yellow circle
                cv2.putText(img, "green", (i[0], i[1]), 1, 1.5, (255, 255, 255), 2)
            traffic_stat = "green"

    
    #If red color detected, find circle from red mask image and show 'red' text
    if maskR.any():
        circles = cv2.HoughCircles(maskR, cv2.HOUGH_GRADIENT, 4, 20,
                                   param1=100, param2=100, minRadius=0, maxRadius=0)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # put text in detected yellow circle
                cv2.putText(img, "red", (i[0], i[1]), 1, 1.5, (255, 255, 255), 2)
            traffic_stat = "red"

    print(traffic_stat)

    cv2.imshow('img',draw_temp)
    cv2.imshow('green', resG)
    cv2.imshow('Red', resR)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
