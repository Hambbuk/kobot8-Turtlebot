#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import numpy
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int8
from a_tunnel.msg import Data
import copy

sensor_data = Data()
rospy.init_node('sensor', anonymous=True)
pub = rospy.Publisher('/sensor_data', Data, queue_size = 100)
rate = rospy.Rate(10)
#scan data recive
def callback(scan):
    #tunnel호출을 받으면 실행 할 수 있는 if문 및 서브스크리버 추가 필요
    Front = scan.ranges[0:14] + scan.ranges[345:359]
    Left1 = scan.ranges[15:34]
    Left2 = scan.ranges[35:54]
    Left3 = scan.ranges[55:74]
    Left4 = scan.ranges[75:94]
    Right1 = scan.ranges[325:344]
    Right2 = scan.ranges[305:324]
    Right3 = scan.ranges[285:304]
    Right4 = scan.ranges[265:284]
    back = scan.ranges[95:264]

    #average
    Front_avg = avge(Front)
    Left1_avg = avge(Left1)
    Left2_avg = avge(Left2)
    Left3_avg = avge(Left3)
    Left4_avg = avge(Left4)
    Right1_avg = avge(Right1)
    Right2_avg = avge(Right2)
    Right3_avg = avge(Right3)
    Right4_avg = avge(Right4)
    back_avg = avge(back)

    avg = [Front_avg, Left1_avg, Left2_avg, Left3_avg, Left4_avg, Right1_avg, Right2_avg, Right3_avg, Right4_avg, back_avg]

    sensor_data.data = avg
    pub.publish(sensor_data)

#if 0 & inf -> no count
def avge(arr):
    l = []
    for i in arr:
        if i == float("inf"):
            continue
        elif i == 0:
            continue
        else:
            l.append(i)
    #print(l)
    return sum(l)/(len(l)+0.01)

def scan_sensor():
    #rospy.Subscriber('/stage',Int8,checking_stage)
    while not rospy.is_shutdown():
        rospy.loginfo("scan data sub and pub")
        rospy.Subscriber('/scan', LaserScan, callback)
        rate.sleep()
	
if __name__ == '__main__':
	try:	
		scan_sensor()
	except rospy.ROSInterruptException:
		pass