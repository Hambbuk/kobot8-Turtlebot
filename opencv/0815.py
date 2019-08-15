import cv2
import numpy as np
import rospy
from geometry_msgs.msg import Twist

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)

lastError = 0
MAX_VEL = 0.12

def t_move(linear, angular):
    twist = Twist()
    twist.linear.x = linear
    twist.angular.z = angular
    pub.publish(twist)

video = cv2.VideoCapture(-1)
rospy.init_node('line_test')

f_list = [(-1, -1)]
s_list = [(999, 999)]

while True:
    ret, orig_frame = video.read()
    if not ret:
        video = cv2.VideoCapture(0)
        continue

    draw_temp = orig_frame.copy()

    cuttingImg = draw_temp[350:, :]

    draw_temp = cuttingImg

    M = np.ones(draw_temp.shape, dtype="uint8") * 30
    draw_temp = cv2.subtract(draw_temp, M)

    frame = cv2.GaussianBlur(draw_temp, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    low_yellow = np.array([20, 100, 50])
    up_yellow = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, low_yellow, up_yellow)
    edges = cv2.Canny(mask, 75, 150)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 360, 100, 100, maxLineGap=50)

    if lines is not None:
	del f_list[:]
        for line in lines:
            x1, y1, x2, y2 = line[0]
            f_list.append((x1,y1))
            f_list.append((x2,y2))
        cv2.circle(frame, max(f_list), 10, (0,0,255), -1)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)


    lower_white = np.array([0, 0, 150])
    upper_white = np.array([255, 50, 255])

    mask = cv2.inRange(hsv, lower_white, upper_white)
    edges = cv2.Canny(mask, 75, 150)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 360, 100,100, maxLineGap=50)
    if lines is not None:
	del s_list[:]
        for line in lines:
            x1, y1, x2, y2 = line[0]
            s_list.append((x1,y1))
            s_list.append((x2,y2))

        cv2.circle(frame, min(s_list), 10, (255,255,0), -1)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)


    # cv2.line(frame, ((w_x1+y_x1)//2, (w_y1+y_y1)//2),((w_x2+y_x2)//2,(y_y2+w_y2)//2),(0, 255, 255), 4)
    (x1, y1) = min(s_list)
    (x2, y2) = max(f_list)
    ave = (x1 + x2) / 2
    cv2.circle(frame, ((x1+x2)//2,(y1+y2)//2) , 10, (200,200,25), -1)
    #print("s_list : ", min(s_list))
    error = ave-315
    #print(error, " error")
    Kp = 0.004
    Kd = 0.025
    print(error)
    angular_z = Kp * error + Kd * (error - lastError)
    #print(angular_z, "is angular_z")
    lastError = error
    linear_x = min(MAX_VEL * ((1 - abs(error) / 500) ** 2.2), 0.2)
    #print(linear_x, " is linear_x")
    angular_z = -min(angular_z, 2.0) if angular_z<0 else -max(angular_z, -2.0)
    #print(angular_z, " is twist angular_z")
    
    t_move(linear_x, angular_z)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(25)
    if key == 27:
	t_move(0,0)
        break

video.release()
cv2.destroyAllWindows()
