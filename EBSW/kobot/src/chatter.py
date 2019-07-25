#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
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


