#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :get_raw_data.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

'''
    * 简单的统计
    × 1. 统计出来一共有多少user/item/position
    × 2. 统计出来多少购买/点击/收藏/购物车
    × 3. 内积！？
'''
import sys
sys.path.append("..")

from util.read_conf import config
from csv import DictReader
from pickle import dump,load
import gzip


raw_data = config('../conf/raw_data.conf')
usr_path = raw_data['usr_train_path']
item_path = raw_data['item_train_path']

def get_statistic_user(s_path):
    "get the num of the usr/item/position/purchase  etc"
    
    print 'open the ',s_path,' file.'
    infile = open(s_path,'rb')
    
    usr_dict = {}
    item_dict = {}
    pos_dict = {}
    cat_dict = {}
    pur_dict = {'1':0,'2':0,'3':0,'4':0}

    print 'start to counts the counts.'

    for idx,row in enumerate(DictReader(infile)):
        #user_id item_id behavior_type user_geohash item_category time

        if row['user_id'] in usr_dict:
            usr_dict[row['user_id']] += 1
        else:
            usr_dict[row['user_id']] = 1

        if row['item_id'] in item_dict:
            item_dict[row['item_id']] += 1
        else:
            item_dict[row['item_id']] = 1

        if row['user_geohash'] in pos_dict:
            pos_dict[row['user_geohash']] += 1
        else:
            pos_dict[row['user_geohash']] = 1

        if row['item_category'] in cat_dict:
            cat_dict[row['item_category']] += 1
        else:
            cat_dict[row['item_category']] = 1

        pur_dict[row['behavior_type']] += 1

        if (idx+1)%1000000 == 0:
            print (idx+1)/1000000,'m usr_item counted.'

    print 'usr_counts',len(usr_dict),' item_counts ',len(item_dict),'total category:',len(cat_dict),' pos_counts ',len(pos_dict),'purchase',pur_dict['1'],pur_dict['2'],pur_dict['3'],pur_dict['4']


def get_statistic_item(inpath):
    "get the sum of the item information"

    print 'open the ',inpath,' file.'
    infile = open(inpath,'rb')
    
    item_dict = {}
    pos_dict = {}
    cat_dict = {}
    
    for idx,row in enumerate(DictReader(infile)):
        #user_id item_id behavior_type user_geohash item_category time

        if row['item_id'] in item_dict:
            item_dict[row['item_id']] += 1
        else:
            item_dict[row['item_id']] = 1

        if row['item_geohash'] in pos_dict:
            pos_dict[row['item_geohash']] += 1
        else:
            pos_dict[row['item_geohash']] = 1

        if row['item_category'] in cat_dict:
            cat_dict[row['item_category']] += 1
        else:
            cat_dict[row['item_category']] = 1

        if (idx+1)%1000000 == 0:
            print (idx+1)/1000000,'m usr_item counted.'

    print 'item_counts ',len(item_dict),'pos_counts ',len(pos_dict),'totoal _cat',len(cat_dict)


if __name__ == '__main__':
    get_statistic_user(usr_path)
    get_statistic_item(item_path)
