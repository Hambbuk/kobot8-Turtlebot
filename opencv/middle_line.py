import cv2
import numpy as np

y_data1 = []
y_data2 = []
w_data1 = []
w_data2 = []


def b_clean(video):
    for i in range(6):
        video.read()


def white_line(frame):
    sensitivity = 15
    # low_white = np.array([0, 0, 255 - sensitivity])
    # up_white = np.array([255, sensitivity, 255])
    low_white = np.array([0, 0, 180])
    up_white = np.array([25, 36, 255])
    w_mask = cv2.inRange(hsv, low_white, up_white)
    edges = cv2.Canny(w_mask, 75, 150)

    lines1 = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)
    if lines1 is not None:
        for i in range(len(lines1)):
            x1 = lines1[i][0][0]
            y1 = lines1[i][0][1]
            x2 = lines1[i][0][2]
            y2 = lines1[i][0][3]

            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)
            print((x1, y1), (x2, y2))


def yellow_line(frame):
    low_yellow = np.array([18, 40, 140])
    up_yellow = np.array([48, 255, 255])
    y_mask = cv2.inRange(hsv, low_yellow, up_yellow)
    edges = cv2.Canny(y_mask, 75, 150)

    lines1 = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)

    if lines1 is not None:
        for i in range(len(lines1)):
            x1 = lines1[i][0][0]
            y1 = lines1[i][0][1]
            x2 = lines1[i][0][2]
            y2 = lines1[i][0][3]

            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)
            print((x1, y1), (x2, y2))


if __name__ == '__main__':
    video = cv2.VideoCapture(2)
    b_clean(video)

    video.set(3, 320)
    video.set(4, 240)

    while True:
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
        sensitivity = 15
        low_white = np.array([0, 0, 255 - sensitivity])
        up_white = np.array([255, sensitivity, 255])
        w_mask = cv2.inRange(hsv, low_white, up_white)
        edges = cv2.Canny(w_mask, 75, 150)

        lines1 = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)

        if lines1 is not None:
            w_data1.clear()
            w_data2.clear()

            for i in range(len(lines1)):
                x1 = lines1[i][0][0]
                y1 = lines1[i][0][1]
                x2 = lines1[i][0][2]
                y2 = lines1[i][0][3]

                w_data1.append([x1, y1])
                w_data2.append([x2, y2])
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)

        else:
            print("previous w: ", w_data1, "\t", w_data2)

        # yellow detection
        low_yellow = np.array([18, 40, 140])
        up_yellow = np.array([48, 255, 255])
        y_mask = cv2.inRange(hsv, low_yellow, up_yellow)
        edges = cv2.Canny(y_mask, 75, 150)

        lines1 = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)

        if lines1 is not None:
            y_data1.clear()
            y_data2.clear()
            for i in range(len(lines1)):
                x1 = lines1[i][0][0]
                y1 = lines1[i][0][1]
                x2 = lines1[i][0][2]
                y2 = lines1[i][0][3]

                y_data1.append([x1, y1])
                y_data2.append([x2, y2])
                cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                # cv2.line(frame, (x1 + 160, y1), (x2 + 60, y2), (0, 148, 148), 5)
                print((x1, y1), (x2, y2))
        else:
            print("previous y: ", y_data1, "\t", y_data2)

        # try:
        #
        #     w_x1 = w_data1[0][0]
        #     y_x1 = y_data1[0][0]
        #     w_y1 = w_data1[0][1]
        #     y_y1 = y_data1[0][1]
        #
        #     w_x2 = w_data2[0][0]
        #     y_x2 = y_data2[0][0]
        #     w_y2 = w_data2[0][1]
        #     y_y2 = y_data2[0][1]
        #
        #     cv2.line(frame, (w_x1 - y_x1, w_y1), (w_x2 - y_x2, w_y2), (180, 255, 255), 5)
        #
        # except IndexError:
        #     w_x1 = 160
        #     y_w1 = 160
        #
        #     cv2.line(frame, (w_x1 - y_x1, w_y1 - y_y1), (w_x2 - y_x2, w_y2 - y_y2), (180, 255, 255), 5)

        cv2.line(frame, (160, 0), (160, 240), (0, 255, 0), 5)

        key = cv2.waitKey(25)
        if key == 27:
            break

        cv2.imshow('frame', frame)
        # cv2.imshow('roi', ROI)

    video.release()
    cv2.destroyAllWindows()
