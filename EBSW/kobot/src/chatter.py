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

ref = db.reference() #
#ref.update({'test' : 'chk'}) #

print(ref.get()) #
print("test")
