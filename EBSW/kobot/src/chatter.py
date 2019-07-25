#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import std_msgs/Float32
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Firebase database 연동
cred = credentials.Certificate('/home/kmucs/Downloads/ebsw.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://ebsw-283e9.firebaseio.com/'
})


#기본위치
sec_0 = db.reference('sector_0') #
sec_1 = db.reference('sector_1') #
sec_2 = db.reference('sector_2') #
sec_3 = db.reference('sector_3') #

#ref.update({'test' : 'chk'}) #

print(sec_0.get())
sec_0_x, sec_0_y = sec_0.get().split()
sec_1_x, sec_1_y = sec_1.get().split()
sec_2_x, sec_2_y = sec_2.get().split()
sec_3_x, sec_3_y = sec_3.get().split()


def send_msg():
    #노드 초기화
    pub = rospy.Publisher('chatter', Float32, queue_size=10)
    rospy.init_node('send_msg', anonymous = True)
    #메시지를 보내는 주기 -> 30분?
    rate = rospy.Rate(10) # 10hz - > 초당 10번

    #노드가 꺼지지 않을때 까지 반복
    while not rospy.is_shutdown():
        test_number = -4.0
        rospy.loginfo('-4.0을 보낸다')
        pub.publish(test_number)
        rate.sleep()

if __name__ == '__main__':
    try:
        send_msg()
    except rospy.ROSInterruptExcettion:
        pass