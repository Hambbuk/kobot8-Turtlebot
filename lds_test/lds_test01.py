import rospy
from sensor_msgs.msg import LaserScan
import numpy as np
global MIN_SCAN_ANGLE_RAD
global MAX_SCAN_ANGLE_RAD
global TURN_SPEED_MPS
MIN_SCAN_ANGLE_RAD = (-90.0) / 180.0 * np.pi
MAX_SCAN_ANGLE_RAD = (+90.0) / 180.0 * np.pi
TURN_SPEED_MPS = 1.57
rospy.Subscriber('/scan', LaserScan, callback)
scan = LaserScan()
#minIndex = np.ceil((MIN_SCAN_ANGLE_RAD - scan.angle_min) / scan.angle_increment)

"""def callback(msg):
 print("Value at 0 degress : " + msg.ranges[0])
 print("Value at 90 degress : " + msg.ranges[360])
 print("Value at 180 degress : " + msg.ranges[719])

rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()"""

print(MIN_SCAN_ANGLE_RAD)
print(scan)
print(scan.angle_increment)
