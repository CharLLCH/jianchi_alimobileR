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

from datetime import datetime

class item:
    __slots__ = ['user_id', 'item_id', 'behavior_type','user_geohash','item_category','week','date','hour']

    def __init__(self,uid,iid,behavior,icat,time,ugeo=None):
        self.user_id = uid
        self.item_id = iid
        self.behavior_type = behavior
        self.user_geohash = ugeo
        self.item_category = icat
        self.week = datetime(int(time[0:4]),int(time[5:7]),int(time[8:10]))
        time = time.split()
        self.date = time[0]
        self.hour = time[1]

        if self.week in ['Saturday','Sunday']:
            self.week_f = 'Weekend'
        else:
            self.week_f = 'Worked'
        num_hour = int(self.hour)
        if num_hour > 5 and num_hour <= 8:
            feat_hour = 'I'
        elif num_hour > 8 and num_hour <= 11:
            feat_hour = 'II'
        elif num_hour > 11 and num_hour <= 14:
            feat_hour = 'III'
        elif num_hour > 14 and num_hour <= 18:
            feat_hour = 'IV'
        elif num_hour > 18 and num_hour <= 23:
            feat_hour = 'V'
        else:
            feat_hour = 'VI'
        self.hour_f = feat_hour

    def get_field_dict(self):
        #fields = ['u_id', 'i_id', 'b_type','u_geo','i_cat']
        fields = ['i_cat']
        f_dict = dict.fromkeys(fields,0)
        #f_dict['u_geo'] = self.user_geohash
        f_dict['i_cat'] = self.item_category
        return f_dict

    def new_feat(self):
        fields = ['u_geo','i_cat','week','hour']
        f_dict = dict.fromkeys(fields,0)
        f_dict['u_geo'] = self.user_geohash
        f_dict['i_cat'] = self.item_category
        f_dict['week'] = self.week_f
        #f_dict['date'] = self.date
        f_dict['hour'] = self.hour_f
        return f_dict


    def __str__(self):
        s = "UserId:%s || ItemID:%s || UserBehavior:%s || UserGeo:%s || ItemCategory:%s || Time:%s-%s || W_H_F:%s-%s\n" \
                %(self.user_id,self.item_id,self.behavior_type,self.user_geohash,self.item_category,self.date,self.hour,self.week_f,self.hour_f)
        return s

    def sql_str(self):
        geo = 'ns'
        if len(self.user_geohash) >= 1:
            geo = self.user_geohash
        return "insert into user_train values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" \
                %(self.user_id,self.item_id,self.behavior_type,self.user_geohash,self.item_category,self.date,self.hour,self.week_f,self.hour_f)
