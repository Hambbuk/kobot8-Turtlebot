import rospy
from sensor_msgs.msg import LaserScan
import numpy as np

"""
1. 터널에 들어오면 초기좌표를 (0, 0)으로 설정해준다
2. 전방과 후방을 나누고, 전방을 몇분할로 나눌것인지
    전방 190도 후방 170도로 나누고 전방을 9분할? -> 맨 앞 30도를 제외하고 160도를 8분할
    20도씩 나누자

3. 왼쪽으로 45도만큼 이동(작년 대회 기준 출구)
4. 회전행렬을 사용하여 앞으로 이동하는 좌표를 터널 입장시에 형성되는
   로컬좌표의 단위벡터에 의거해서 변환하여 보여준다?
5. 터들봇의 위치에 따라서 출구방향을 바라봐야하는 각도가 달라진다.
   따라서 로컬 좌표와 출구 좌표의 기울어진 각도를 구해서 목표 각도를 만든다.
6. 터틀봇이 바라보는 방향에 따라서 목표 각도의 왼쪽 오른쪽 판단하여 회전방향을 정함
7. 장애물이 있을때는 왼쪽 오른쪽을 구분하여 거리가 먼쪽으로 회전
8. 만약 터틀봇 사이드에 벽이 있다면 벽을 피하기 위해 벽의 반대방향으로 방향을 설정하여 이동과 동시에 회전을 한다.
"""

def callback(scan):
    Front = scan.ranges[0:14] + scan.ranges[345:359] #전방
    Left_1 = scan.ranges[15:34]
    Left_2 = scan.ranges[35:54]
    Left_3 = scan.ranges[55:74]
    Left_4 = scan.ranges[75:94]
    Rigth_1 = scan.ranges[325:344]
    Rigth_2 = scan.ranges[305:324]
    Rigth_3 = scan.ranges[285:304]
    Rigth_4 = scan.ranges[265:284]
    back = scan.ranges[95:264]

    #average
    avg(Front)
    avg(Left_1)
    avg(Left_2)
    avg(Left_3)
    avg(Left_4)
    avg(Right_1)
    avg(Right_2)
    avg(Right_3)
    avg(Right_4)


#if 0 & inf -> no count
def avg(arr):
    l = [i for i in arr if( i is not 0 or i is not float("inf"))]
    return sum(l)/len(l)


rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()
