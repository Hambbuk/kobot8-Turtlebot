# -*- coding: utf-8 -*- # 한글 주석쓰려면 이거 해야함
import cv2  # opencv 사용
import numpy as np
import rospy
from geometry_msgs.msg import Twist

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
lastError = 0
MAX_VEL = 0.12
left_x = 0
right_x = 0

def t_move(linear, angular):
    twist=Twist()
    twist.linear.x=linear
    twist.angular.z=angular
    pub.publish(twist)

def grayscale(img):  # 흑백이미지로 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def canny(img, low_threshold, high_threshold):  # Canny 알고리즘
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):  # 가우시안 필터
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):  # ROI 셋팅

    mask = np.zeros_like(img)  # mask = img와 같은 크기의 빈 이미지

    if len(img.shape) > 2:  # Color 이미지(3채널)라면 :
        color = color3
    else:  # 흑백 이미지(1채널)라면 :
        color = color1

    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움
    cv2.fillPoly(mask, vertices, color)

    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):  # 선 그리기
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def draw_fit_line(img, lines, color=[255, 0, 0], thickness=10):  # 대표선 그리기
    slope = (lines[3] - lines[1]) / (lines[2] - lines[0])

    b = (-1) * slope * lines[2] + lines[3]

    u = int((-1000 - b) / slope)
    lll = int((1000 - b) / slope)

    cv2.line(img, (lll, 1000), (u, -1000), color, thickness)


def draw_cross_line(img, line1, line2):
    # 교점 찾기
    _line1 = {"slope": (line1[3] - line1[1]) / (line1[2] - line1[0])}
    _line1["intercept"] = (-1) * _line1["slope"] * line1[2] + line1[3]

    _line2 = {"slope": (line2[3] - line2[1]) / (line2[2] - line2[0])}
    _line2["intercept"] = (-1) * _line2["slope"] * line2[2] + line2[3]

    # _cross = [x, 1000,  x, -1000]
    _line1X1 = int((1000 - _line1["intercept"]) / _line1["slope"])
    _line2X1 = int((1000 - _line2["intercept"]) / _line2["slope"])
    x1 = (_line1X1 + _line2X1) // 2
    _line1X2 = int((-1000 - _line1["intercept"]) / _line1["slope"])
    _line2X2 = int((-1000 - _line2["intercept"]) / _line2["slope"])
    x2 = (_line1X2 + _line2X2) // 2

    cv2.line(img, (x1, 1000), (x2, -1000), (0, 255, 0), 3)

    pass


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):  # 허프 변환
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    # line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    # draw_lines(line_img, lines)

    return lines


def weighted_img(img, initial_img, a=1, b=1., c=0.):  # 두 이미지 operlap 하기
    return cv2.addWeighted(initial_img, a, img, b, c)


def get_fitline(img, f_lines):  # 대표선 구하기
    lines = np.squeeze(f_lines)
    lines = lines.reshape(lines.shape[0] * 2, 2)
    rows, cols = img.shape[:2]
    output = cv2.fitLine(lines, cv2.DIST_L2, 0, 0.01, 0.01)
    vx, vy, x, y = output[0], output[1], output[2], output[3]
    x1, y1 = int(((img.shape[0] - 1) - y) / vy * vx + x), img.shape[0] - 1
    x2, y2 = int(((img.shape[0] / 2 + 100) - y) / vy * vx + x), int(img.shape[0] / 2 + 100)

    result = [x1, y1, x2, y2]
    return result


if __name__ == '__main__':
    rospy.init_node('line_test')
    cap = cv2.VideoCapture(-1)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 160)
    
    height, width = int(cap.get(4)), int(cap.get(3))

    i = 0
    while True:
        ret, image = cap.read()

        ret, image = cap.read()
        ret, image = cap.read()
        ret, image = cap.read()
        ret, image = cap.read()

        draw_temp = image.copy()
        cuttingImg = draw_temp[350:,:]
        draw_temp = cuttingImg
        M = np.ones(draw_temp.shape, dtype="uint8") *20
        draw_temp = cv2.subtract(draw_temp, M)


        print(i)
        i+=1

        if ret:
            cv2.imshow("pp", image)

            # bird eye tramformation
            # white yellow


            try:
                gray_img = grayscale(draw_temp)  # 흑백이미지로 변환

                blur_img = gaussian_blur(gray_img, 3)  # Blur 효과

                canny_img = canny(blur_img, 70, 210)  # Canny edge 알고리즘

                vertices = np.array(
                    [[(50, height), (width / 2 - 45, height / 2 + 60), (width / 2 + 45, height / 2 + 60),
                      (width - 50, height)]],
                    dtype=np.int32)
                ROI_img = canny_img  # ROI 설정

                line_arr = hough_lines(ROI_img, 1, 1 * np.pi / 180, 30, 10, 20)  # 허프 변환
                line_arr = np.squeeze(line_arr)

                # 기울기 구하기

                slope_degree = (np.arctan2(line_arr[:, 1] - line_arr[:, 3],
                                           line_arr[:, 0] - line_arr[:, 2]) * 180) / np.pi

                # 수평 기울기 제한
                line_arr = line_arr[np.abs(slope_degree) < 160]
                slope_degree = slope_degree[np.abs(slope_degree) < 160]
                # 수직 기울기 제한
                line_arr = line_arr[np.abs(slope_degree) > 95]
                slope_degree = slope_degree[np.abs(slope_degree) > 95]
                # 필터링된 직선 버리기
                L_lines, R_lines = line_arr[(slope_degree > 0), :], line_arr[(slope_degree < 0), :]
                temp = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
                L_lines, R_lines = L_lines[:, None], R_lines[:, None]
                # 왼쪽, 오른쪽 각각 대표선 구하기
                left_fit_line = get_fitline(image, L_lines)
                right_fit_line = get_fitline(image, R_lines)
                # 대표선 그리기
                draw_fit_line(temp, left_fit_line)
                draw_fit_line(temp, right_fit_line)

                draw_cross_line(temp, left_fit_line, right_fit_line)

                result = weighted_img(temp, image)  # 원본 이미지에 검출된 선 overlap
                error = ave_theta - 87.5
                print(ave_theta, " ave_theta")
                Kp = 0.006	
                Kd = 0.0085
		
                angular_z = Kp * error + Kd * (error - lastError)
                print(angular_z, "is angular_z")
                lastError = error
                linear_x = min(MAX_VEL * ((1 - abs(error) / 500) ** 2.2), 0.2)
                print(linear_x, " is linear_x")
                angular_z = min(angular_z, 2.0) if angular_z<0 else max(angular_z, -2.0)
                print(angular_z, " is twist angular_z")
		
                t_move(linear_x, angular_z)
                cv2.imshow('result', result)  # 결과 이미지 출력


            except:
                center_x = (left_x + right_x)/2
                center = center_x
                #print(center)
                error  = center
                print(error, " is error")
                Kp = 0.0020
                Kd = 0.010

                angular_z = Kp * error + Kd * (error - lastError)
                lastError = error
                linear_x = min(MAX_VEL * ((1-abs(error) / 500 ) ** 2.2), 0.2)
                print(linear_x, " is linear_x")
                angular_z = -max(angular_z, -2.0) if angular_z<0 else -min(angular_z, 2.0)
                print(angular_z, " is angular_z")

                t_move(linear_x, angular_z)

            k = cv2.waitKey(1) & 0xFF

            if k == 27:
                break
            pass

            pass
        else:
            #print(1)
            pass

        pass

    cap.release()
    cv2.destroyAllWindows()

    pass
