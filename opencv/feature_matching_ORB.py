# Feature matching code to detect parking sign, blocking bar using ORB.

import numpy as np
import cv2
# from matplotlib import pyplot as plt

cap = cv2.VideoCapture(2)

while True:

    # covert video frame to HSV
    _, img2 = cap.read()

    #bluring for eliminate noises

    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img1 = cv2.imread('images/parking_not_allowed.png',0)
    # img2 = cv2.imread('images/TrafficLight.jpg',0)

    # Initiate ORB detector
    orb = cv2.ORB_create()

    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    #Match descriptors
    matches = bf.match(des1, des2)
    #Sort them in the order of their distance
    matches = sorted(matches, key=lambda x:x.distance)

    #Draw first 10 matches
    img3= cv2.drawMatches(img1, kp1, img2, kp2, matches[:10], img1, flags=2)
    cv2.imshow('img3', img3)

    cv2.imshow('img2', img2)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
