#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 # opencv 사용
import numpy as np
import rospy
from std_msgs.msg import Int8
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
global stage
stage = -1 #(0=신호, 1=삼거리-left, 2=삼거리-right, 3=공사, 4=주차, 5=차단바, 6=터널, 100=라인트레이싱)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)

def t_move(linear, angular):
    twist = Twist()
    twist.linear.x = linear
    twist.angular.z = angular
    pub.publish(twist)

def avg(data):
	return 	sum(data)/(len(data)-data.count(0)+0.01)

############################################################################################################3

def SinHo(sinho_msg):
    global stage
    #초록불을 받았다면
    if(sinho_msg.data == 1):
        print("sinho")
        stage = 100

############################################################################################################3

def SamGeoRi(samgeori_msg):
    global stage
    #왼쪽간판
    if(samgeori_msg.data == 1):
        stage = 1
        print("1")
        t_move(0, 0)
    #오른쪽간판
    elif(samgeori_msg.data == 2):
        stage = 2
        print("2")
        t_move(0, 0)

############################################################################################################3

def GongSa_move(data):
    SensorData = data.ranges
    Front = SensorData[1:5]+SensorData[355:359]
    front = avg(Front)
    print(front)
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
    if(gongsa_msg.data == 3):
        stage = 3
        print("3")
        #rospy하드코딩하는 부분
        GongSa_move()

############################################################################################################3

def JuCha(jucha_msg):
    global stage
    if(jucha_msg.data == 4):
        stage = 4
        #rospy하드코딩하는 부분

############################################################################################################3

def ChaDanBar(chadanbar_msg):
    global stage
    if(chadanbar_msg.data == 5):
        print("test")
        #초음파 센서 받아서 사용하는 부분

############################################################################################################3

def Tunnel(tunnel_msg):
    global stage
    if(tunnel_msg.data == 6):
        stage = 6
        
############################################################################################################3

rospy.init_node('main_node')

def linstener():
    while not rospy.is_shutdown():
        rospy.Subscriber('/SinHo_msg', Int8, SinHo)
        rospy.Subscriber('/stage', Int8, SamGeoRi)
        rospy.Subscriber('/stage', Int8, GongSa)
        #rospy.Subscriber("/scan" , LaserScan , GongSa_move)
        #rospy.Subscriber('/stage', Int8, JuCha)
    #rospy.Subscriber('/stage', Int8, ChaDanBar)
    #rospy.Subscriber('/stage', Int8, Tunnel)
        rospy.sleep(rospy.Duration(0.1))
        rospy.spin()


if __name__ == '__main__':
    linstener()
