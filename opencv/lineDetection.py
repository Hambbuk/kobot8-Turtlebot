import numpy as np
import cv2

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# threshold: 입력이미지가 그레이 스케일 이미지여야 한다.

#  ADAPTIVE_THRESH_MEAN_C와 함께 adaptiveThreshold 함수를 사용하면 앞에서 검은색으로 검출된 부분의 글씨가 검출됩니다.
# 첫번째 아규먼트는 원본 이미지, 두번째 아규먼트는 임계값 이상일 경우 픽셀값, 세번째 아규먼트는 적응형 이진화 타입,
# 네번째 아규먼트는 이진화 타입, 다섯째 아규먼트는 임계값 계산시 함께 볼 주변 픽셀의 범위를 블럭 크기로 지정,
# 여섯번째 아규먼트는 평균 또는 가중평균에서 뺄 값입니다.

while True:

    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

    ret, img_result1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    ret, img_result2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    for i in range(len(lines)):
        print(i)
        for rho, theta in lines[i]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            cv2.line(img_result1, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # ret, img_result2 = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    cv2.imshow("VideoFrame", frame)
    cv2.imshow("THRESH_BINARY", img_result1)
    # cv2.imshow("THRESH_OTSU", img_result2)

    if cv2.waitKey(1) > 0: break

camera.release()
cv2.destroyAllWindows()
