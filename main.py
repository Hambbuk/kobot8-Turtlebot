#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 # opencv 사용
import numpy as np
import rospy
from std_msgs.msg import Int8

global stage
stage = 0 #(0=신호, 1=삼거리, 2=공사, 3=주차, 4=차단바, 5=터널, 100=라인트레이싱)

def t_move(linear, angular):
    twist = Twist()


def SinHo(sinho_msg):
    global stage
    #초록불을 받았다면
    if(sinho_msg.data == 1):
        stage = 100
        pub.publish(stage)

def SamGeoRi(samgeori_msg):
    global stage
    #왼쪽간판
    if(samgeori_msg.data == 1):
        stage = 1
    #오른쪽간판
    elif(samgeori_msg.data == 2):
        stage = 1

def GongSa(gongsa_msg):
    global stage
    #공사모드에 진입
    if(gongsa_msg.data == 1):
        stage = 2
        pub.publish(stage)
        #rospy하드코딩하는 부분

def JuCha(jucha_msg):
    global stage
    if(jucha_msg.data = 1):
        stage = 3
        pub.publish(stage)
        #rospy하드코딩하는 부분

def ChaDanBar(chadanbar_msg):
    global stage
    if(chadanbar_msg.data = 1):
        #초음파 센서 받아서 사용하는 부분

def Tunnel(tunnel_msg):
    global stage
    if(tunnel_msg.data == 1):
        stage = 5
        pub.publish(stage)


rospy.init_node('main_node')

rospy.Subscriber('/SinHo_msg', Int8, SinHo)
rospy.Subscriber('/SamGeoRi_msg', Int8, SamGeoRi)
rospy.Subscriber('/GongSa_msg', Int8, GongSa)
rospy.Subscriber('/JuCha_msg', Int8, JuCha)
rospy.Subscriber('/ChaDanBar_msg', Int8, ChaDanBar)
rospy.Subscriber('/Tunnel_msg', Int8, Tunnel)

pub = rospy.Publisher('/stage', UInt8, queue_size=1000)
rospy.spin()
