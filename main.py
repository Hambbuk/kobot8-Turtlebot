#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 # opencv 사용
import numpy as np
import rospy
from std_msgs.msg import Int8

global stage
stage = 0 #(0=신호, 1=삼거리, 2=공사, 3=주차, 4=차단바, 5=터널, 100=라인트레이싱)

def SinHo(sinho_msg):
    #초록불을 받았다면
    if(sinho_msg.data == 1):
        stage = 100

def SamGeoRi(samgeori_msg):
    #왼쪽간판
    if(samgeori_msg.data == 1):


    #오른쪽간판
    elif(samgeori_msg.data == 2):

def GongSa(gongsa_msg):
    


rospy.init_node('main_node')
rospy.Subscriber('/SinHo_msg', Int8, SinHo)
rospy.Subscriber('/SamGeoRi_msg', Int8, SamGeoRi)


#pub = rospy.Publisher('/detect/tunnel_stamped', UInt8, queue_size=1)
#pub.publish(msg)
rospy.spin()
