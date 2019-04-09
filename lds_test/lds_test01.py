#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import numpy as np

global MIN_SCAN_ANGLE_RAD
global MAX_SCAN_ANGLE_RAD
global TURN_SPEED_MPS
MIN_SCAN_ANGLE_RAD = (-90.0) / 180.0 * np.pi
MAX_SCAN_ANGLE_RAD = (+90.0) / 180.0 * np.pi
TURN_SPEED_MPS = 1.57

def callback(scan_msg):
    minIndex = np.ceil((MIN_SCAN_ANGLE_RAD - scan_msg.angle_min) / scan_msg.angle_increment)
    maxIndex = np.floor((MAX_SCAN_ANGLE_RAD - scan_msg.angle_min)/ scan_msg.angle_increment)
    midIndex = (minIndex+maxIndex)/2
    #print(maxIndex)
    closestRange_left=scan_msg.ranges[int(minIndex)]
    print(closestRange_left)

rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()

if __name__ == '__main__':
    callback()
