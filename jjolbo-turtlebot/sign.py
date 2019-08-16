__author__ = 'jjolbo'

import cv2
import numpy as np
# kind = int(input())


cap = cv2.VideoCapture(0)

# sign = ['park','left','right','turnel']

def template_matching(frame,template, val):

    # for idx in range(len(sign)):
    #     if idx == val:
    #         print(sign[idx])

    w, h = template.shape[::-1]

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.7)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)

if __name__ == '__main__':

    while True:
        _, frame = cap.read()

        M = np.ones(frame.shape, dtype="uint8") * 50
        subtracted = cv2.subtract(frame, M)
        cv2.imshow('d', subtracted)

        copy_frame1 = frame.copy()
        copy_frame2 = frame.copy()
        copy_frame3 = frame.copy()
        copy_frame4 = frame.copy()

        # park_template = cv2.imread("표지판.png", cv2.IMREAD_GRAYSCALE)
        # template_matching(copy_frame1, park_template, 0)

        left_template = cv2.imread("left.png", cv2.IMREAD_GRAYSCALE)
        template_matching(copy_frame2, left_template, 1)

        # right_template = cv2.imread("right.png", cv2.IMREAD_GRAYSCALE)
        # template_matching(copy_frame3, right_template, 2)

        # turnel_template = cv2.imread("터널.png", cv2.IMREAD_GRAYSCALE)
        # template_matching(copy_frame4, turnel_template, 3)

        # cv2.imshow('copy_frame1', copy_frame1)
        cv2.imshow('copy_frame2', copy_frame2)
        # cv2.imshow('copy_frame3', copy_frame3)
        # cv2.imshow('copy_frame4', copy_frame4)

        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
