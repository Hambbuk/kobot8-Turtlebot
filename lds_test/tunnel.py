import rospy
import tf
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import numpy as np
from tf.transformations import euler_from_quaternion, quaternion_from_euler


global pose
global past
global past_num
global dot
global cnt
cnt = 0
dot = [0, 0]
past = [[0, 0]]
pose = [0, 0]
rospy.init_node('scan_values')

#################################################################################################################################
#scan data recive
def callback(scan):
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

    return avg;

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

#################################################################################################################################
#check left wall
def scan_Left_Wall(arr):
    cnt = 0
    for i in range(1, 5):
        if arr[i] < 0.2 and arr[i] > 0:
            cnt = cnt + 1
    if cnt >= 3:
        return 1
    else:
        return 0;

def scan_Right_Wall(arr):
    cnt = 0
    for i in range(5, 9):
        if arr[i] < 0.2 and arr[i] > 0:
            cnt = cnt + 1
    if cnt >= 3:
        return 1
    else:
        return 0;

def scan_Front_Wall(arr):
    cnt = 0
    for i in range(0, 3):
        if arr[i] < 0.2 and arr[i] > 0:
            cnt = cnt + 1
    if cnt >= 2:
        return 1
    else:
        return 0;

#################################################################################################################################
#Subscriber odom
def call_test(odom):
    r_late = rospy.Rate(10)
    list = [odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w]
    theta = euler_from_quaternion(list)
    print(theta)
    r_late.sleep()

#store_pose
def store_pose():
	global pose
	global past
    global past_num
	global cnt

	if cnt == 0:
		if flag2==0:
			copy_pose = copy.copy(pose)	# store the place coordinate which turtlebot must avoid
			past.append(copy_pose)		# ex) entrance of tunnel
			past_number.append(0)
			num = num+1
			flag2 = 1

#past pose check
def past_check():
    global pose
    global past
    global past_num
    global cnt
    for i in range(0, len(pasr)):
        X = abs(pose[0] - past[i][0])
        Y = abs(pose[1] - past[i][1])

        if X>0.1 and Y>0.1:
            past_num[i] = 1 #?

        if X<0.1 and Y<0.1: #좌표가 왔던곳이라면
            if past_num[i] == 1: #
                rospy.loginfo([X, Y])
                pase_num[i] = 0
    return 0;

#################################################################################################################################
#same place rotation
def destination1(data1):
	if data1==1:
		twist.linear.x = 0.0
		twist.angular.z = 0.6
		pub.publish(twist)
	elif data1==3:
		twist.linear.x = 0.0
		twist.angular.z = -0.6            #Right (-) Left (+)
		pub.publish(twist)

#go
def destination4(data1):
	if data1==1:
		twist.linear.x = 0.04
		twist.angular.z = 0.3
		pub.publish(twist)
	elif data1==3:
		twist.linear.x = 0.04
		twist.angular.z = -0.3            #Right (-) Left (+)
		pub.publish(twist)

#back
def destination5(data1):
	if data1==1:
		twist.linear.x = -0.01
		twist.angular.z = 0.6
		pub.publish(twist)
	elif data1==3:
		twist.linear.x = -0.01
		twist.angular.z = -0.6            #Right (-) Left (+)
		pub.publish(twist)

#################################################################################################################################

def recive():
    rospy.Subscriber('/scan', LaserScan, callback)
    rospy.Subscriber('/odom', Odometry, call_test)
    rospy.spin()

if __name__ == '__main__':
    recive()
