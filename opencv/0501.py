import cv2
import numpy as np
import rospy
from geometry_msgs.msg import Twist

y_data1 = []
y_data2 = []
w_data1 = []
w_data2 = []
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
def t_move(linear, angular):
    twist=Twist()
    twist.linear.x=linear
    twist.angular.z=angular
    pub.publish(twist)

def b_clean(video):
    for i in range(6):
        video.read()

#
# def white_line(frame):
#     sensitivity = 15
#     # low_white = np.array([0, 0, 255 - sensitivity])
#     # up_white = np.array([255, sensitivity, 255])
#     low_white = np.array([0, 0, 180])
#     up_white = np.array([25, 36, 255])
#     w_mask = cv2.inRange(hsv, low_white, up_white)
#     edges = cv2.Canny(w_mask, 75, 150)
#
#     lines1 = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)
#     if lines1 is not None:
#         for i in range(len(lines1)):
#             x1 = lines1[i][0][0]
#             y1 = lines1[i][0][1]
#             x2 = lines1[i][0][2]
#             y2 = lines1[i][0][3]
#
#             cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)
#             print((x1, y1), (x2, y2))
#
#
# def yellow_line(frame):
#     low_yellow = np.array([18, 40, 140])
#     up_yellow = np.array([48, 255, 255])
#     y_mask = cv2.inRange(hsv, low_yellow, up_yellow)
#     edges = cv2.Canny(y_mask, 75, 150)
#
#     lines1 = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)
#
#     if lines1 is not None:
#         for i in range(len(lines1)):
#             x1 = lines1[i][0][0]
#             y1 = lines1[i][0][1]
#             x2 = lines1[i][0][2]
#             y2 = lines1[i][0][3]
#
#             cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)
#             print((x1, y1), (x2, y2))


if __name__ == '__main__':
    video = cv2.VideoCapture(0)
    b_clean(video)

    video.set(3, 320)
    video.set(4, 240)

    max_yel_x1 = 0
    max_yel_x2 = 0
    while True:
        linex = 0
        cnt = 0
        ret, orig_frame = video.read()
        if not ret:
            video = cv2.VideoCapture(0)
            continue


        frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
        # frame = frame[70:150, 0:320]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # yellow_line(frame)
        # white_line(frame)

        # white detection

        sensitivity = 10
        low_white = np.array([0, 0, 255 - sensitivity])
        up_white = np.array([255, sensitivity, 255])
        w_mask = cv2.inRange(hsv, low_white, up_white)
        edges = cv2.Canny(w_mask, 75, 150)

        lines1 = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)

        # point = [
        #     {"x":-1, "y":0},
        #     {"x": -1, "y": 0}
        # ]

        if lines1 is not None:
            #w_data1.clear()
            #w_data2.clear()
            cnt += len(lines1)
            for i in range(len(lines1)):
                x1 = lines1[i][0][0]
                y1 = lines1[i][0][1]
                x2 = lines1[i][0][2]
                y2 = lines1[i][0][3]

                # if x2 > point[0]:
                #     point[0] = x2
                #     point[2] = x1
                #     point[1] = y2
                #     point[3] = y1
                #     pass

                w_data1.append([x1, y1])
                w_data2.append([x2, y2])
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)
                linex = linex + x2
        else:
            print("else")
            #print("previous w: ", w_data1, "\t", w_data2)

        # yellow detection
        low_yellow = np.array([18, 20, 190])
        up_yellow = np.array([48, 255, 255])
        y_mask = cv2.inRange(hsv, low_yellow, up_yellow)
        edges = cv2.Canny(y_mask, 75, 150)

        lines1 = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)

        if lines1 is not None:
            #y_data1.clear()
            #y_data2.clear()
            cnt += len(lines1)
            for i in range(len(lines1)):
                x1 = lines1[i][0][0]
                y1 = lines1[i][0][1]
                x2 = lines1[i][0][2]
                y2 = lines1[i][0][3]

                y_data1.append([x1, y1])
                y_data2.append([x2, y2])

                max_yel_x1 = max(y_data1)
                max_yel_x2 = max(y_data2)
                cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                linex = linex + x2
                # cv2.line(frame, (x1 + 160, y1), (x2 + 60, y2), (0, 148, 148), 5)


        # cv2.line(frame, (max_yel_x1, y_data1[0][1]), (max_yel_x2, y_data2[0][1]), (255,0,0), 5)

        cv2.line(frame, (160, 0), (160, 240), (0, 255, 0), 5)
        lin = linex / cnt
        if(lin > 158 or lin < 162):
            t_move(0.22, 0)
            print("go! : ", lin)
        elif(lin > 162):
            t_move(0.22, 0.1)
            print("right! : ", lin)
        else:
            t_move(0.22)
            print("left! : ", len)

        key = cv2.waitKey(25)
        if key == 27:
            break

        cv2.imshow('frame', frame)
        # cv2.imshow('roi', ROI)

    video.release()
    cv2.destroyAllWindows()
