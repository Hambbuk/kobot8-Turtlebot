#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'jjolbo'

import cv2
import rospy
import numpy as np
from std_msgs.msg import Int8
import sinho

#(0=신호, 1=left, 2=right, 3=공사, 4=주차, 5=차단바, 6=터널, 100=라인트레이싱)

cap = cv2.VideoCapture(1)
cap.set(3, 400)
cap.set(4, 225)
pub_stage = rospy.Publisher('/stage', Int8, queue_size=5)
#pub_stage.publish(stage)

def template_matching(frame,template,flag):
    w, h = template.shape[::-1]

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.7)

    for pt in zip(*loc[::-1]):
        flag += 1
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
        if flag == 1:
            return flag

if __name__ == '__main__':
    rospy.init_node('cap_node', anonymous=True)
    

    while True:
        flag_right = 0
        flag_left = 0
        flag_stop = 0
        flag_gongsa = 0
        flag_parking = 0
        flag_tunnel = 0

        stage = -1

        _, frame = cap.read()
        M = np.ones(frame.shape, dtype="uint8") * 90
        sinho.traffic_light(frame)

        copy_frame1 = frame.copy()
        copy_frame2 = frame.copy()
        copy_frame3 = frame.copy()
        copy_frame4 = frame.copy()
        copy_frame5 = frame.copy()
        copy_frame6 = frame.copy()

        #left
        left_template = cv2.imread("left.png", cv2.IMREAD_GRAYSCALE)
        flag_left = template_matching(copy_frame1, left_template, flag_left)
        if flag_left == 1:
            #ros_code
            pub_stage.publish(1)

        #right
        right_template = cv2.imread("right.png", cv2.IMREAD_GRAYSCALE)
        flag_right = template_matching(copy_frame2, right_template, flag_right)
        if flag_right == 1:
            #ros_code
            pub_stage.publish(2)

        #stop        
        stop_template = cv2.imread("stop.png", cv2.IMREAD_GRAYSCALE)
        flag_stop = template_matching(copy_frame3, stop_template, flag_stop)
        if flag_stop == 1:
            #ros_code
            pub_stage.publish(3)

        #gongsa
        gongsa_template = cv2.imread("gongsa.png", cv2.IMREAD_GRAYSCALE)
        flag_gongsa = template_matching(copy_frame4, gongsa_template, flag_gongsa)
        if flag_gongsa == 1:
            #ros_code
            pub_stage.publish(4)

        #parking
        parking_template = cv2.imread("park_sign.png", cv2.IMREAD_GRAYSCALE)
        flag_parking = template_matching(copy_frame5, parking_template, flag_parking)
        if flag_parking == 1:
            #ros_code
            pub_stage.publish(5)

        #tunnel
        turnel_template = cv2.imread("turnnel.png", cv2.IMREAD_GRAYSCALE)
        flag_tunnel = template_matching(copy_frame6, turnel_template, flag_tunnel)
        if flag_tunnel == 1:
            #ros_code
            pub_stage.publish(6)


        cv2.imshow('copy_frame1', copy_frame1)
        cv2.imshow('copy_frame2', copy_frame2)
        # cv2.imshow('copy_frame3', copy_frame3)
        # cv2.imshow('copy_frame4', copy_frame4)
        # cv2.imshow('copy_frame5', copy_frame5)
        # cv2.imshow('copy_frame6', copy_frame6)

        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
