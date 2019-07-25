#!/usr/bin/env python

from sensor_msgs.msg import LaserScan

import rospy

def laserCallback(data):
	rospy.loginfo("msg subscribed")

def listener():
	rospy.init_node('ros_controller' , anonymous = True)
	rospy.Subscriber("scan" , LaserScan , laserCallback)

	rospy.spin()


if __name__ == '__main__':
	listener()
