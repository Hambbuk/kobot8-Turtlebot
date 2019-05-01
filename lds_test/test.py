import rospy
from sensor_msgs.msg import LaserScan
import numpy as np

def callback(scan):
    Front = scan.ranges[0:14] + scan.ranges[345:359]
    Left_1 = scan.ranges[15:34]
    Left_2 = scan.ranges[35:54]
    Left_3 = scan.ranges[55:74]
    Left_4 = scan.ranges[75:94]
    Rigth_1 = scan.ranges[325:344]
    Rigth_2 = scan.ranges[305:324]
    Rigth_3 = scan.ranges[285:304]
    Rigth_4 = scan.ranges[265:284]
    back = scan.ranges[95:264]

    #average
    avg(Front)
    avg(Left_1)
    avg(Left_2)
    avg(Left_3)
    avg(Left_4)
    avg(Right_1)
    avg(Right_2)
    avg(Right_3)
    avg(Right_4)


#if 0 & inf -> no count
def avg(arr):
    l = [i for i in arr if( i is not 0 or i is not float("inf"))]
    return sum(l)/len(l)


rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()
