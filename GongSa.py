import numpy as np
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
rospy.init_node('sensor', anonymous=True)

def avg(data):
	return 	sum(data)/(len(data)-data.count(0)+0.01)

def callback(data):
    SensorData = data.ranges
    Front = SensorData[1:15]+SensorData[345:359]
    front = avg(Front)
    print(front)

rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
