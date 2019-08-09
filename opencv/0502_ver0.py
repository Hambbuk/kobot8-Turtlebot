# detect only yellow line
import cv2
import numpy as np
import rospy
from geometry_msgs.msg import Twist

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)

lastError = 0
MAX_VEL = 0.13
left_x = 0
right_x = 0

def t_move(linear, angular):
    twist=Twist()
    twist.linear.x=linear
    twist.angular.z=angular
    pub.publish(twist)

def b_clean(video):
    for i in range(6):
        video.read()

if __name__ == '__main__':
    rospy.init_node('line_test')
    video = cv2.VideoCapture(-1)
    #video.set(cv2.CAP_PROP_IOS_DEVICE_WHITEBALANCE, 5000000000)
    #video.awb_mode = 'off'

    video.set(3, 480)
    video.set(4, 720)
    while True:
        ret, orig_frame = video.read()
        if not ret:
            video = cv2.VideoCapture(-1)
            continue

        draw_temp = orig_frame.copy()
	cuttingImg = draw_temp[250:, :]
	draw_temp = cuttingImg
	M = np.ones(draw_temp.shape, dtype="uint8") * 50
	draw_temp = cv2.subtract(draw_temp, M)

        frame = cv2.GaussianBlur(draw_temp, (5, 5), 0)
	#frame = frame - 30
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        lower_yellow = np.array([18, 40, 140])
        upper_yellow = np.array([48, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        yellow_mask = cv2.erode(yellow_mask, None, iterations=1)
        yellow_mask = cv2.dilate(yellow_mask, None, iterations=1)

        edges = cv2.Canny(yellow_mask, 50, 150, apertureSize=3)

        lines = cv2.HoughLines(edges, 1, np.pi / 180, 3)

        y_theta = 0     # variable of degree y ( 0' ~ 180' )

        if lines is not None:
            for rho, theta in lines[0]:
                y_theta = 90-(theta * 180 / np.pi)
                if y_theta<0 : y_theta+=180
                y_theta_real = y_theta*np.pi/180    # variable of degrre y for drawing lines ( 0 ~ pi )
                # print('yellow-', 'rho: ', rho, '\t\ttheta: ' ,theta)
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
            cv2.line(draw_temp, (x1, y1), (x2, y2), (45, 255, 180), 2)  #detect yellow -> draw yellow
            # cv2.line(draw_temp, (x1, y1), (x2, y2), (255, 0, 0), 2)
        else:
            y_theta_real = np.pi/2
            y_theta = 90



        print('yellow ', y_theta)

        #sensitivity = 3
        lower_white = np.array([0, 0, 150])
        upper_white = np.array([255, 50, 255])
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        white_mask = cv2.erode(white_mask, None, iterations=1)
        white_mask = cv2.dilate(white_mask, None, iterations=1)

        edges = cv2.Canny(white_mask, 50, 150, apertureSize=3)

        lines = cv2.HoughLines(edges, 1, np.pi / 180, 3)

        w_theta = 0     # variable of degree w ( 0' ~ 180' )
        if lines is not None:
            for rho, theta in lines[0]:
                w_theta = 90-(theta* 180 / np.pi)
                if w_theta<0 : w_theta+=180
                w_theta_real = w_theta*np.pi /180    # variable of degrre w for drawing lines ( 0 ~ pi )
                # print('white-', 'rho: ', rho, '\t\ttheta: ', theta)
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

            cv2.line(draw_temp, (x1, y1), (x2, y2), (255, 0, 0), 2)     #detect white -> draw blue
        else:   # default average degree 90'
            w_theta_real = np.pi/2
            w_theta = 90

        print('white ', w_theta)
        ave_theta = (y_theta + w_theta)/2        # variable of average degree ( 0' ~ 180' )
        ave_theta_real = (y_theta_real + w_theta_real)/2     # variable of average degree for drawing lines ( 0 ~ pi )



        print('ave_theta = ', ave_theta)
        # ave_theta = ave_theta
        a_f = 636
        b_f = 478
        p = 1000
        lineThickness = 2
        cv2.line(draw_temp, (int(a_f/2-p*np.cos(ave_theta_real)), b_f+int(p*np.sin(ave_theta_real))), (int((a_f/2+p*np.cos(ave_theta_real))), b_f-int(p*np.sin(ave_theta_real))), (0, 255, 0), lineThickness)
        # cv2.line(draw_temp, (int(a_f/2-p*np.sin(ave_theta)), b_f+int(p*np.cos(ave_theta))), (int((a_f/2+p*np.sin(ave_theta))), b_f-int(p*np.cos(ave_theta))), (0, 255, 0), lineThickness)
		
		
        error  = ave_theta - 85
        print(error, " is error")
        Kp = 0.006
        Kd = 0.007

        angular_z = Kp * error + Kd * (error - lastError)
	print(angular_z, "is angular_z")
        lastError = error
        linear_x = min(MAX_VEL * ((1-abs(error) / 500 ) ** 2.2), 0.2)
        print(linear_x, " is linear_x")
        #angular_z = min(angular_z, 2.0) if angular_z<0 else max(angular_z, -2.0)
        #print(angular_z, " is twist angular_z")

        t_move(linear_x, angular_z)

        cv2.imshow('edges', draw_temp)


        key = cv2.waitKey(25)
        if key == 27:
            t_move(0, 0)
            break

    video.release()
    cv2.destroyAllWindows()
