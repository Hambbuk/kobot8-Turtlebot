import time
import cv2
import numpy as np
import threading
import Queue

# ROS
import rospy
from geometry_msgs.msg import Twist

# pub_linear = rospy.Publish('linear', Float64, queue_size=5)
# pub_angular = rospy.Publish('angular', Float64, queue_size=5)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
MAX_VEL = 0.15


def t_move(linear, angular):
    twist = Twist()
    twist.linear.x = linear
    twist.angular.z = angular
    pub.publish(twist)
    pass


def threadJHLineTracer(cam_obj):
    MAX_VEL = 0.15

    f_list = [(-1, -1)]
    s_list = [(999, 999)]
    frame_count_w = frame_count_y = last_error = 0

    t = threading.currentThread()
    while getattr(t, "run", True):
        frame_count_w += 1
        frame_count_y += 1

        ret, orig_frame = cam_obj.get_line_frame()

        if not ret:
            break

        draw_temp = orig_frame.copy()
        cutting_img = draw_temp[360:, :]
        y_roi = draw_temp[360:, :250]
        w_roi = draw_temp[360:, 310:]

        M = np.ones(y_roi.shape, dtype="uint8") * 90
        y_roi = cv2.subtract(y_roi, M)

        min_lab = np.array([84, 110, 128])
        min_lab = np.array([195, 140, 220])

        # Convert the BGR image to other color spaces
        img_lab = cv2.cvtColor(y_roi, cv2.COLOR_BGR2LAB)
        img_lab = cv2.GaussianBlur(img_lab, (5, 5), 0)

        mask_lab_yellow = cv2.inRange(img_lab, min_lab, min_lab)
        mask_lab_yellow = cv2.erode(mask_lab_yellow, None, iterations=1)
        mask_lab_yellow = cv2.dilate(mask_lab_yellow, None, iterations=3)

        result_lab = cv2.bitwise_and(y_roi, y_roi, mask=mask_lab_yellow)
        edges = cv2.Canny(result_lab, 75, 150)
        #         # cv2.imshow('yellow edges', edges)

        lines = cv2.HoughLinesP(edges, 1, np.pi / 360, 50, 10, maxLineGap=150)

        if lines is not None:
            del f_list[:]
            for line in lines:
                x1, y1, x2, y2 = line[0]
                f_list.append((x1, y1))
                f_list.append((x2, y2))
            cv2.circle(y_roi, max(f_list), 10, (0, 0, 255), -1)
            cv2.line(y_roi, (x1, y1), (x2, y2), (0, 255, 0), 4)

        # if frame_count_y > 5:
        #    del f_list[:]
        #    f_list.append((0,1))

        M1 = np.ones(w_roi.shape, dtype="uint8") * 90
        w_roi = cv2.subtract(w_roi, M1)
        min_lab = np.array([89, 112, 104])
        min_lab = np.array([198, 142, 137])

        img_lab = cv2.cvtColor(w_roi, cv2.COLOR_BGR2LAB)
        img_lab = cv2.GaussianBlur(img_lab, (5, 5), 0)

        mask_lab_white = cv2.inRange(img_lab, min_lab, min_lab)
        mask_lab_white = cv2.erode(mask_lab_white, None, iterations=1)
        mask_lab_white = cv2.dilate(mask_lab_white, None, iterations=3)

        result_lab1 = cv2.bitwise_and(w_roi, w_roi, mask=mask_lab_white)
        edges = cv2.Canny(result_lab1, 75, 150)
        # cv2.imshow('white edges', edges)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 360, 50, 10, maxLineGap=150)

        if lines is not None:
            del s_list[:]
            for line in lines:
                x1, y1, x2, y2 = line[0]
                s_list.append((x1 + 310, y1))
                s_list.append((x2 + 310, y2))

            (c_x, c_y) = min(s_list)
            cv2.circle(w_roi, (c_x - 310, c_y), 10, (255, 255, 0), -1)
            cv2.line(w_roi, (x1, y1), (x2, y2), (0, 0, 255), 4)

        # if frame_count_w > 5:
        #    del s_list[:]
        #    s_list.append((640,1))
        # cv2.line(frame, ((w_x1+y_x1)//2, (w_y1+y_y1)//2),((w_x2+y_x2)//2,(y_y2+w_y2)//2),(0, 255, 255), 4)
        (x1, y1) = min(s_list)
        (x2, y2) = max(f_list)

        # if(x1 >= x2):
        #   x2 = 120
        if (310 < x1 < 340) and (220 < x2 < 250):
            if y1 > y2:
                x1 = 550
            elif y1 < y2:
                x2 = 100
        # print('y;', x2)
        # print('w:', x1)
        ave = (x1 + x2) // 2

        cv2.circle(cutting_img, ((x1 + x2) // 2, (y1 + y2) // 2), 10, (200, 0, 25), -1)
        # cv2.imshow("frame", cutting_img)
        # cv2.imshow('yroi', y_roi)
        # cv2.imshow('wroi', w_roi)

        #         # print("s_list : ", min(s_list))
        error = ave - 300
        # print(error)
        # # print(error, " error")
        ros_kp = 0.0055
        ros_kd = 0.0075
        #         # print(error)
        angular_z = ros_kp * error + ros_kd * (error - last_error)
        #         # print(angular_z, "is angular_z")
        last_error = error
        linear_x = min(MAX_VEL * ((1 - abs(error) / 500) ** 2.2), 0.2)
        #         # #print(linear_x, " is linear_x")
        angular_z = -min(angular_z, 2.0) if angular_z < 0 else -max(angular_z, -2.0)
        #         # print(angular_z, " is twist angular_z")

        # pub_linear.publish(linear_x)
        # pub_angular.publish(angular_z)

        #         # print(draw_temp.shape)
        t_move(linear_x, angular_z)

        if chr(cv2.waitKey(1) & 255) == 'q':
            t_move(0, 0)
            break
        pass

    t_move(0, 0)
    pass


class KOBOT_CAM(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.line_cam = cv2.VideoCapture(-1)
        self.line_cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.line_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.obstacle_cam = cv2.VideoCapture(1)
        self.obstacle_cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.obstacle_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        self.line_cam_frames = Queue.Queue(4)
        self.obstacle_cam_frames = Queue.Queue(4)

        ret1, frame1 = self.line_cam.read()
        self.line_cam_frames.put(frame1)

        ret2, frame2 = self.obstacle_cam.read()
        self.obstacle_cam_frames.put(frame2)
        pass

    def run(self):
        self._thread_get_frame()

    def _thread_get_frame(self):
        while True:
            ret1, frame1 = self.line_cam.read()
            self.line_cam_frames.put(frame1)

            ret2, frame2 = self.obstacle_cam.read()
            self.obstacle_cam_frames.put(frame2)
        pass

    def get_line_frame(self):
        return True, self.line_cam_frames.get()

    def get_obstacle_frame(self):
        return True, self.obstacle_cam_frames.get()

    pass


if __name__ == '__main__':
    cam_obj = KOBOT_CAM()
    cam_obj.start()
    # time.sleep(3)

    rospy.init_node('line_test')

    # Mission 1 :
    thread_line_tracing = threading.Thread(target=threadJHLineTracer, args=(cam_obj,))
    thread_line_tracing.start()

    while True:
        ret, frame = cam_obj.get_obstacle_frame()
        if not ret:
            break

        if chr(cv2.waitKey(1) & 255) == 'q':
            break

        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # lower mask (0-10)
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

        # upper mask (170-180)
        lower_red = np.array([170, 50, 50])
        upper_red = np.array([180, 255, 255])
        mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

        # join my masks
        mask = mask0 + mask1

        count = cv2.countNonZero(mask)

        h, w, _ = img_hsv.shape

        print(count * 100 / (h * w))

        if count * 100 / (h * w) > 60:
            break

        pass

    thread_line_tracing.run = False
    thread_line_tracing.join()
    t_move(0, 0)
    pass

# rospy.Subscriber('/stage', Int8, line)
# rospy.spin()
