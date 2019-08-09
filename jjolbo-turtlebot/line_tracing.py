# -*- coding: utf-8 -*- # 한글 주석쓰려면 이거 해야함
import cv2  # opencv 사용
import numpy as np


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
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    # draw_lines(img, lines)

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
    cap = cv2.VideoCapture(-1)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 160)
    cap.set(5, 60)
    height, width = int(cap.get(4)), int(cap.get(3))

    i = 0
    while True:
        ret, image = cap.read()

        ret, image = cap.read()
        ret, image = cap.read()
        ret, image = cap.read()
        ret, image = cap.read()


        if ret:
            cv2.imshow("pp", image)

            # bird eye tramformation
            # white yellow


            try:
                gray_img = grayscale(image)  # 흑백이미지로 변환

                blur_img = gaussian_blur(gray_img, 3)  # Blur 효과

                canny_img = canny(blur_img, 70, 210)  # Canny edge 알고리즘

                vertices = np.array(
                    [[(50, height), (width / 2 - 45, height / 2 + 60), (width / 2 + 45, height / 2 + 60),
                      (width - 50, height)]],
                    dtype=np.int32)
                ROI_img = canny_img  # ROI 설정

                line_arr = hough_lines(ROI_img, 1, 1 * np.pi / 180, 30, 10, 20)  # 허프 변환
                # print(type(line_arr[0][0]))
                # print(line_arr.dtype)

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
                cv2.imshow('result', result)  # 결과 이미지 출력


            except Exception as e:
                # print(e)
                copy_img = image.copy()

                frame = cv2.GaussianBlur(copy_img, (5, 5), 0)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                low_yellow = np.array([18, 40, 140])
                up_yellow = np.array([48, 255, 255])
                yellow_mask = cv2.inRange(hsv, low_yellow, up_yellow)
                yellow_mask = cv2.erode(yellow_mask, None, iterations=1)
                yellow_mask = cv2.dilate(yellow_mask, None, iterations=1)

                edges = cv2.Canny(yellow_mask, 50, 150, apertureSize=3)

                lines = cv2.HoughLines(edges, 1, np.pi / 180, 3)

                y_theta = 0

                y_theta = 0
                yellow_check = False
                if lines is not None:
                    for rho, theta in lines[0]:
                        yellow_check = True
                        y_theta = 90 - (theta * 180 / np.pi)
                        if y_theta < 0: y_theta += 180
                        y_theta_real = y_theta * np.pi / 180  # variable of degrre y for drawing lines ( 0 ~ pi )
                        # print('yellow-', 'rho: ', rho, '\t\ttheta: ' ,theta)
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a * rho
                        y0 = b * rho
                        x1 = int(x0 + 1000 * (-b))
                        y1 = int(y0 + 1000 * (a))
                        x2 = int(x0 - 1000 * (-b))
                        y2 = int(y0 - 1000 * (a))

                    print('yellow check', yellow_check)
                    cv2.line(copy_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.line(copy_img, (x1+ 250, y1+ 250), (x2+ 250, y2+ 250), (0, 255, 255), 2)

                    cv2.line(copy_img, ((x1+ x1+ 250)//2, (y1+y1+250)//2), ((x2+x2+250)//2, (y2+y2+250)//2), (255,255,0), 2)

                    # ave_theta = (y_theta + w_theta) / 2  # variable of average degree ( 0' ~ 180' )
                    # ave_theta_real = (y_theta_real + w_theta_real) / 2  # variable of average degree for drawing lines ( 0 ~ pi )
                    #
                    # a_f = 636
                    # b_f = 478
                    # p = 1000
                    # lineThickness = 2
                    # cv2.line(copy_img,
                    #          (int(a_f / 2 - p * np.cos(ave_theta_real)), b_f + int(p * np.sin(ave_theta_real))),
                    #          (int((a_f / 2 + p * np.cos(ave_theta_real))), b_f - int(p * np.sin(ave_theta_real))),
                    #          (0, 255, 0), lineThickness)
                    #


                else:
                    print('yellow check', yellow_check)

                sensitivity = 15
                lower_white = np.array([0, 0, 255 - sensitivity])
                upper_white = np.array([255, sensitivity, 255])
                white_mask = cv2.inRange(hsv, lower_white, upper_white)
                white_mask = cv2.erode(white_mask, None, iterations=1)
                white_mask = cv2.dilate(white_mask, None, iterations=1)

                edges = cv2.Canny(white_mask, 50, 150, apertureSize=3)

                lines = cv2.HoughLines(edges, 1, np.pi / 180, 3)
                w_theta = 0

                white_check = False
                if lines is not None:
                    for rho, theta in lines[0]:
                        white_check = True
                        w_theta = theta * 180 / np.pi
                        # print('white-', 'rho: ', rho, '\t\ttheta: ', theta)
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a * rho
                        y0 = b * rho
                        x1 = int(x0 + 1000 * (-b))
                        y1 = int(y0 + 1000 * (a))
                        x2 = int(x0 - 1000 * (-b))
                        y2 = int(y0 - 1000 * (a))

                    print('white check', white_check)
                    cv2.line(copy_img, (x1, y1), (x2, y2), (255, 0, 0), 2)

                else:
                    print('white check', white_check)
                    # cv2.line(copy_img,(581, 0 ),(581, 473), (255, 0, 255), 2 )



                cv2.imshow('error', copy_img)
                pass

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
