#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float32
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from kobot.msg import Msg

global x1, y1, x2, y2, x3, y3, sector_num, s1_pm100, s2_pm100, s3_pm100

#Firebase database 연동
cred = credentials.Certificate('/home/kmucs/Downloads/ebsw.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://ebsw-283e9.firebaseio.com/'
})

def sector_chk():
    #80보다 클때만 실행
    global s1_pm100, s2_pm100, s3_pm100, sector_num
    sector_num = 0;
    arr = [s1_pm100, s2_pm100, s3_pm100]
    max_num = max(arr)
    if(max_num>80):
        idx = arr.index(max_num)
        sector_num = idx + 1

def db_chk():
    global x1, y1, x2, y2, x3, y3, s1_pm100, s2_pm100, s3_pm100, sector_num

    #자표변수
    s1 = db.reference('u_data/pose/s1') #-4 -1
    s2 = db.reference('u_data/pose/s2') #3 1
    s3 = db.reference('u_data/pose/s3') #0 -2

    x1, y1 = map(float, s1.get().split())
    x2, y2 = map(float, s2.get().split())
    x3, y3 = map(float, s3.get().split())

    #미세먼지 변수
    pm1 = db.reference('u_data/pm/s1')
    pm2 = db.reference('u_data/pm/s2')
    pm3 = db.reference('u_data/pm/s3')

    s1_pm25, s1_pm100 = map(float, pm1.get().split())
    s2_pm25, s2_pm100 = map(float, pm2.get().split())
    s3_pm25, s3_pm100 = map(float, pm3.get().split())

def pose_msg():
    global x1, y1, x2, y2, x3, y3, sector_num

    #퍼블리셔 및 메시지 생성
    pub_pose = rospy.Publisher("pose", Msg, queue_size=1000)
    msg = Msg()

    #노드 초기화
    rospy.init_node('pose_msg', anonymous = True)

    #1초에 10번씩 수행
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        #db값 체크
        db_chk()
        sector_chk()
        msg.x1 = x1
        msg.y1 = y1
        msg.x2 = x2
        msg.y2 = y2
        msg.x3 = x3
        msg.y3 = y3
        msg.sector_number = sector_num
        
        #값 확인
        # rospy.loginfo(msg.x1)
        # rospy.loginfo(msg.y1)
        # rospy.loginfo(msg.x2)
        # rospy.loginfo(msg.y2)
        # rospy.loginfo(msg.x3)
        # rospy.loginfo(msg.y3)
        rospy.loginfo("sengind")

        #값 퍼블리셔
        pub_pose.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.loginfo("pose_msg")
        pose_msg()
    except rospy.ROSInterruptException:
        pass