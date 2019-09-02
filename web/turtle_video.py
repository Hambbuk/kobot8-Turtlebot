import cv2
import numpy as np
global lastError
lastError = 0
global MAX_VEL
MAX_VEL = 0.12

global f_list
f_list = [(-1, -1)]
global s_list
s_list = [(999, 999)]

def line_trace(orig_frame):
    global lastError
    global MAX_VEL
    global f_list
    global s_list


    #sinho.traffic_light(orig_frame)

    #sign._main(orig_frame)
    draw_temp = orig_frame.copy()
    cuttingImg = draw_temp[360:, :]
    y_ROI = draw_temp[360:, :250]
    w_ROI = draw_temp[360:, 310:]

    M = np.ones(y_ROI.shape, dtype="uint8") * 80
    y_ROI = cv2.subtract(y_ROI, M)


    minLAB = np.array([4, 106, 90])
    maxLAB = np.array([203, 224, 219])

    # Convert the BGR image to other color spaces
    imageLAB = cv2.cvtColor(y_ROI, cv2.COLOR_BGR2LAB)
    imageLAB = cv2.GaussianBlur(imageLAB, (5, 5), 0)

    maskLABYellow = cv2.inRange(imageLAB, minLAB, maxLAB)
    maskLABYellow = cv2.erode(maskLABYellow, None, iterations=1)
    maskLABYellow = cv2.dilate(maskLABYellow, None, iterations=3)

    resultLAB = cv2.bitwise_and(y_ROI, y_ROI, mask=maskLABYellow)
    edges = cv2.Canny(resultLAB, 75, 150)
    #cv2.imshow('yellow edges', edges)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 360, 80, 10, maxLineGap=150)

    if lines is not None:
        del f_list[:]
        for line in lines:
            x1, y1, x2, y2 = line[0]
            f_list.append((x1, y1))
            f_list.append((x2, y2))
        cv2.circle(y_ROI, max(f_list), 10, (0, 0, 255), -1)
        cv2.line(y_ROI, (x1, y1), (x2, y2), (0, 255, 0), 4)

    #if frame_count_y > 5:
    #    del f_list[:]
    #    f_list.append((0,1))

    M1 = np.ones(w_ROI.shape, dtype="uint8") * 80
    w_ROI = cv2.subtract(w_ROI, M1)
    minLAB = np.array([89, 112, 85])
    maxLAB = np.array([198, 187, 165])

    # minLAB = np.array([29, 112, 67])
    # maxLAB = np.array([197, 190, 162])

    imageLAB = cv2.cvtColor(w_ROI, cv2.COLOR_BGR2LAB)
    imageLAB = cv2.GaussianBlur(imageLAB, (5, 5), 0)

    maskLABWhite = cv2.inRange(imageLAB, minLAB, maxLAB)
    maskLABWhite = cv2.erode(maskLABWhite, None, iterations=1)
    maskLABWhite = cv2.dilate(maskLABWhite, None, iterations=3)

    resultLAB1 = cv2.bitwise_and(w_ROI, w_ROI, mask=maskLABWhite)
    edges = cv2.Canny(resultLAB1, 75, 150)
    # cv2.imshow('white edges', edges)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 360, 70, 10, maxLineGap=150)

    if lines is not None:
        del s_list[:]
        for line in lines:
            x1, y1, x2, y2 = line[0]
            s_list.append((x1 + 310, y1))
            s_list.append((x2 + 310, y2))

        (c_x,c_y) = min(s_list)
        cv2.circle(w_ROI, (c_x-310, c_y), 10, (255, 255, 0), -1)
        cv2.line(w_ROI, (x1, y1), (x2, y2), (0, 0, 255), 4)

    #if frame_count_w > 5:
    #    del s_list[:]
    #    s_list.append((640,1))
    # cv2.line(frame, ((w_x1+y_x1)//2, (w_y1+y_y1)//2),((w_x2+y_x2)//2,(y_y2+w_y2)//2),(0, 255, 255), 4)
    (x1, y1) = min(s_list)
    (x2, y2) = max(f_list)


    #if(x1 >= x2):
    #   x2 = 120
    if (x1 > 310 and x1 < 340) and (x2 > 220 and x2 < 250):
        if y1 > y2:
            x1 = 550
        elif y1 < y2:
            x2 = 100
    # print('y;', x2)
    # print('w:', x1)
    ave = (x1 + x2) // 2
    cv2.circle(cuttingImg, ((x1+x2)//2,(y1+y2)//2) , 10, (200,0,25), -1)

    cv2.imshow("frame", cuttingImg)
    cv2.imshow('yroi', y_ROI)
    cv2.imshow('wroi', w_ROI)

    #print("s_list : ", min(s_list))
    error = ave-330
    #print(error)
    # print(error, " error")
    Kp = 0.006
    Kd = 0.0075
    #print(error)
    angular_z = Kp * error + Kd * (error - lastError)
    #print(angular_z, "is angular_z")
    lastError = error
    linear_x = min(MAX_VEL * ((1 - abs(error) / 500) ** 2.2), 0.2)
    # #print(linear_x, " is linear_x")
    angular_z = -min(angular_z, 2.0) if angular_z<0 else -max(angular_z, -2.0)
    #print(angular_z, " is twist angular_z")

    #pub_linear.publish(linear_x)
    #pub_angular.publish(angular_z)
    return linear_x, angular_z
    #print(draw_temp.shape)
