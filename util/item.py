#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :item.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

'''
    # 类似于user是一个用户所有数据的类，这是一条记录的类
    灵活转变，方便存储db等
    读一条是读，转化成类还可以方便定义一些操作函数！
'''

import datetime 

class item:
    __slots__ = ['user_id', 'item_id', 'behavior_type','user_geohash','item_category','time']

    def __init__(self,uid,iid,behavior,icat,time,ugeo=None):
        self.user_id = uid
        self.item_id = iid
        self.behavior_type = behavior
        self.user_geohash = ugeo
        self.item_category = icat
        self.date = time[8:10]
        self.hour = time[-2:]

    def str(self):
        s = "UserId:%s || ItemID:%s || UserBehavior:%s || UserGeo:%s || ItemCategory:%s || Time:%s-%s \n" \
                %(self.user_id,self.item_id,self.behavior_type,self.user_geohash,self.item_category,self.date,self.hour)
        return s

    def sql_str(self):
        geo = 'ns'
        if len(self.user_geohash) >= 1:
            geo = self.user_geohash
        return "insert into user_train values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" \
                %(self.user_id,self.item_id,self.behavior_type,self.user_geohash,self.item_category,self.date,self.hour)
