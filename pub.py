#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
rospy.init_node('sensor', anonymous=True)
pub_twist = rospy.Publisher('/cmd_vel', Twist, queue_size=5)

def avg(data):
	return 	sum(data)/(len(data)-data.count(0)+0.01)

def t_move(linear, angular):
    twist = Twist()
    twist.linear.x=linear
    twist.angular.z=angular
    pub_twist.publish(twist)



def test_move(data):
    SensorData = data.ranges
    Front = SensorData[1:5]+SensorData[355:359]
    front = avg(Front)
    print(front)
    t_move(0.1, 0)
    if front<0.3:
        print("front")
        rospy.sleep(rospy.Duration(1))
        t_move(0, 1.7)    
        rospy.sleep(rospy.Duration(1))
        t_move(0.13, 0)
        rospy.sleep(rospy.Duration(1))
        t_move(0.13, -1.2)
        rospy.sleep(rospy.Duration(3))
        t_move(0, 0)
        

rospy.Subscriber("/scan" , LaserScan , test_move)
rospy.spin()

