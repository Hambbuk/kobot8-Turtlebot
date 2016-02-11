#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 # opencv 사용
import numpy as np
import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
pub_twist = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
pub_stage = rospy.Publisher('/stage', Int8, queue_size=5)
global stage
stage = 0 #(0=신호, 1=삼거리, 2=공사, 3=주차, 4=차단바, 5=터널, 100=라인트레이싱)

def t_move(linear, angular):
    twist = Twist()

def avg(data):
	return 	sum(data)/(len(data)-data.count(0)+0.01)

def SinHo(sinho_msg):
    global stage
    #초록불을 받았다면
    if(sinho_msg.data == 1):
        stage = 100
        pub_stage.publish(stage)

def SamGeoRi(samgeori_msg):
    global stage
    #왼쪽간판
    if(samgeori_msg.data == 1):
        stage = 1
    #오른쪽간판
    elif(samgeori_msg.data == 2):
        stage = 1

def GongSa_move(data):
    SensorData = data.ranges
    Front = SensorData[1:5]+SensorData[355:359]
    front = avg(Front)
    print(front)
    t_move(0.1, 0)
    if front<0.325:
        print("front")
        rospy.sleep(rospy.Duration(1))
        t_move(0, 1.6)    
        rospy.sleep(rospy.Duration(1))
        t_move(0.11, 0)
        rospy.sleep(rospy.Duration(2))
        t_move(0.0, -1.7)
        rospy.sleep(rospy.Duration(1))
        t_move(0.14, 0)
        rospy.sleep(rospy.Duration(3))
        t_move(0, -1.6)    
        rospy.sleep(rospy.Duration(1))
        t_move(0.11, 0)
        rospy.sleep(rospy.Duration(2))
        t_move(0, 1.7)    
        rospy.sleep(rospy.Duration(1))
        t_move(0.1, 0)    
        rospy.sleep(rospy.Duration(1))

def GongSa(gongsa_msg):
    global stage
    #공사모드에 진입
    if(gongsa_msg.data == 1):
        stage = 2
        pub_stage.publish(stage)
        #rospy하드코딩하는 부분
        GongSa_move()

def JuCha(jucha_msg):
    global stage
    if(jucha_msg.data == 1):
        stage = 3
        pub_stage.publish(stage)
        #rospy하드코딩하는 부분

def ChaDanBar(chadanbar_msg):
    global stage
    if(chadanbar_msg.data == 1):
        print("test")
        #초음파 센서 받아서 사용하는 부분

def Tunnel(tunnel_msg):
    global stage
    if(tunnel_msg.data == 1):
        stage = 5
        pub_stage.publish(stage)


rospy.init_node('main_node')

#if __name__ == '__main__':
#    try:
#        talker()
#    except rospy.ROSInterruptException:
#        pass

print("test")
print(stage, " is stage")
pub_stage.publish(stage)
print("test2")
rospy.Subscriber('/SinHo_msg', Int8, SinHo)
print("test2")
rospy.Subscriber('/SamGeoRi_msg', Int8, SamGeoRi)
print("test2")
rospy.Subscriber('/GongSa_msg', Int8, GongSa)
rospy.Subscriber("/scan" , LaserScan , GongSa_move)
rospy.Subscriber('/JuCha_msg', Int8, JuCha)
rospy.Subscriber('/ChaDanBar_msg', Int8, ChaDanBar)
rospy.Subscriber('/Tunnel_msg', Int8, Tunnel)

pub = rospy.Publisher('/stage', Int8, queue_size=1000)
rospy.spin()
