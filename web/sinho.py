#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Detecting traffic light using HoughCircles - red, yellow, green
import cv2
import rospy
import numpy as np
from std_msgs.msg import Int8

CIRCLE_SIZE = 3000

def traffic_light(frame):
    pub_sinho = rospy.Publisher('/SinHo_msg', Int8, queue_size=5)
    SinHo_msg = 0
    pub_sinho.publish(SinHo_msg)
    # bluring for eliminate noises
    img = frame.copy()

    img = cv2.medianBlur(img, 5)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of color in HSV
    # lowerYellow = np.array([20, 90, 100])
    # upperYellow = np.array([32, 255, 255])
    # upperYellow = np.array([41, 90, 94])

    # lowerGreen = np.array([45, 100, 100])
    # upperGreen = np.array([93, 255, 210])
    # lowerRed = np.array([140, 100, 100])
    # upperRed = np.array([180, 255, 255])

    # from robotis's code
    #
    lowerRed = np.array([-10, 150, 38])
    upperRed = np.array([10, 255, 255])
    lowerYellow = np.array([20, 100, 50])
    upperYellow = np.array([35, 255, 255])
    lowerGreen = np.array([46, 65, 50])
    upperGreen = np.array([90, 255, 255])
    #81 245 253 / 165 2 255

    # Threshold the HSV image to get three of colors
    maskR = cv2.inRange(hsv, lowerRed, upperRed)
    maskY = cv2.inRange(hsv, lowerYellow, upperYellow)
    maskG = cv2.inRange(hsv, lowerGreen, upperGreen)

    resY = cv2.bitwise_and(frame, frame, mask=maskY)
    resG = cv2.bitwise_and(frame, frame, mask=maskG)
    resR = cv2.bitwise_and(frame, frame, mask=maskR)

    traffic_stat = ""

    # If yellow color detected, find circle from yellow mask image and show 'yellow' text
    # if maskY.any():
    #     circles = cv2.HoughCircles(maskY, cv2.HOUGH_GRADIENT, 4, 20,
    #                                param1=100, param2=100, minRadius=0, maxRadius=0)
    #     if circles is not None:
    #         circles = np.uint16(np.around(circles))
    #         for i in circles[0, :]:
    #             # draw the outer circle
    #             cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
    #             # put text in detected yellow circle
    #             cv2.putText(img, "yellow", (i[0], i[1]), 1, 1.5, (255, 255, 255), 2)
    #         traffic_stat = "yellow"

    # If green color detected, find circle from green mask image and show 'green' text
    if maskG.any():
        circles = cv2.HoughCircles(maskG, cv2.HOUGH_GRADIENT, 4, 20,
                                   param1=40, param2=40, minRadius=0, maxRadius=10)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                print('go')
                #input ros code
                SinHo_msg = 1
                pub_sinho.publish(SinHo_msg)
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # put text in detected yellow circle
                cv2.putText(img, "green", (i[0], i[1]), 1, 1.5, (255, 255, 255), 2)
            return 1
                
            traffic_stat = "green"

    # If red color detected, find circle from red mask image and show 'red' text
    if maskR.any():
        circles = cv2.HoughCircles(maskR, cv2.HOUGH_GRADIENT, 4, 20,
                                   param1=100, param2=100, minRadius=0, maxRadius=0)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                print("stop")
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # put text in detected yellow circle
                cv2.putText(img, "red", (i[0], i[1]), 1, 1.5, (255, 255, 255), 2)
            traffic_stat = "red"

    # if maskR.any():
    #     rectangles = cv2.
    print(traffic_stat)

    # cv2.imshow('traffic_light', img)
    # cv2.imshow('Yellow', resY)
    # cv2.imshow('green', resG)
    # cv2.imshow('Red', resR)

#if __name__ == '__main__':
#   cap = cv2.VideoCapture(2)
#    traffic_light(cap)
