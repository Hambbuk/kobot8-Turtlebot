# detect only yellow line
import cv2
import numpy as np
import rospy
from geometry_msgs.msg import Twist

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
def t_move(linear, angular):
    twist=Twist()
    twist.linear.x=linear
    twist.angular.z=angular
    pub.publish(twist)

def b_clean(video):
    for i in range(6):
        video.read()

if __name__ == '__main__':
    rospy.init_node('0502_ver0')
    video = cv2.VideoCapture(0)
    b_clean(video)
    while True:
        ret, orig_frame = video.read()
        if not ret:
            video = cv2.VideoCapture(0)
            continue

        draw_temp = orig_frame.copy()

        frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        lower_yellow = np.array([10, 70, 100])
        upper_yellow = np.array([45, 255, 255])
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

        sensitivity = 15
        lower_white = np.array([0, 0, 255 - sensitivity])
        upper_white = np.array([255, sensitivity, 255])
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

        if ave_theta >= 95:
            print("left")
            t_move(0.15, 0.2)
        elif ave_theta <= 85:
            print("right")
            t_move(0.15, -0.2)
        else:
            print("go")
            t_move(0.15, 0)



        cv2.imshow('edges', draw_temp)


        key = cv2.waitKey(25)
        if key == 27:
            t_move(0, 0)
            break

    video.release()
    cv2.destroyAllWindows()
