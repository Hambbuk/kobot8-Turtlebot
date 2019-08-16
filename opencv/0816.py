import cv2
import numpy as np

video = cv2.VideoCapture(2)

while True:
    ret, orig_frame = video.read()
    if not ret:
        video = cv2.VideoCapture(0)
        continue

    draw_temp = orig_frame.copy()

    cuttingImg = draw_temp[250:, :]

    draw_temp = cuttingImg

    M = np.ones(draw_temp.shape, dtype="uint8") * 90
    draw_temp = cv2.subtract(draw_temp, M)

    frame = cv2.GaussianBlur(draw_temp, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    low_yellow = np.array([20, 100, 50])
    up_yellow = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, low_yellow, up_yellow)
    edges = cv2.Canny(mask, 75, 150)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 360, 100, 100, maxLineGap=50)

    f_list = []
    if lines is not None:
        f_list = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            f_list.append((x1,y1))
            f_list.append((x2,y2))

        cv2.circle(frame, max(f_list), 10, (0,0,255), -1)
        cv2.circle(frame, min(f_list), 10, (0, 0, 255), -1)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
    else:
        f_list = [(0,0)]


    # lower_white = np.array([0, 0, 150])
    # upper_white = np.array([255, 50, 255])
    #
    # mask = cv2.inRange(hsv, lower_white, upper_white)
    # edges = cv2.Canny(mask, 75, 150)
    #
    # s_list = []
    # lines = cv2.HoughLinesP(edges, 1, np.pi / 360, 100,100, maxLineGap=50)
    # if lines is not None:
    #     w_list.clear()
    #     for line in lines:
    #         x1, y1, x2, y2 = line[0]
    #         s_list.append((x1,y1))
    #         s_list.append((x2,y2))
    #
    #         w_list.append([(x1, y1), (x2, y2)])
    #
    #     (x,y) = min(s_list)
    #     cv2.circle(frame, min(s_list), 10, (255,255,0), -1)
    #     cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
    # else:
    #     print(w_list[-1][0])
    #     print(w_list[-1][1])

    (x1,y1) = min(f_list)
    (x2,y2) = max(f_list)
    cv2.circle(frame, ((x1+x2)//2,(y1+y2)//2) , 10, (200,200,25), -1)
    # cv2.line(frame, ((w_x1+y_x1)//2, (w_y1+y_y1)//2),((w_x2+y_x2)//2,(y_y2+w_y2)//2),(0, 255, 255), 4)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(25)
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()
