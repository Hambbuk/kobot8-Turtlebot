import rospy
from sensor_msgs.msg import LaserScan
import numpy as np

def callback(scan):
    print("Value at 0 degress : " , scan.ranges[0])
    print("Value at 90 degress : " , scan.ranges[89])
    print("Value at 180 degress : " , scan.ranges[179])
    print("Value at 270 degress : " , scan.ranges[269])
    print("Value at ranges size : " , len(scan.ranges))


rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()
