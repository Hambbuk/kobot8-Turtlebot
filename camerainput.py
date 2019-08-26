import cv2
import threading
import Queue
import time


class KOBOT_CAM(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.line_cam = cv2.VideoCapture(0)
        self.line_cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.line_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.obstacle_cam = cv2.VideoCapture(1)
        self.obstacle_cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.obstacle_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.line_cam_frames = Queue.Queue(4)
        self.obstacle_cam_frames = Queue.Queue(4)
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
    time.sleep(3)

    while True:
        if chr(cv2.waitKey(1) & 255) == 'q':
            break

        ret13, frame = cam_obj.get_line_frame()
        cv2.imshow("c1", frame)

        ret23, frame1 = cam_obj.get_obstacle_frame()
        cv2.imshow("c2", frame1)
