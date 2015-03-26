#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :split_raw_data.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

'''
    非17-18的，不是4的，且不在17-18-4的u和i的，随便抽2w4
    17-18的，不是4且不和17-18-4对应的u和i冲突的，随便抽2w4
    正例就17 18的所有的 u-i-4
'''
import sys
sys.path.append('..')

from csv import DictReader
from random import random
from util.read_conf import config
import pickle

raw_data = config('../conf/raw_data.conf')
raw_78_path = raw_data['u_te_time']
raw_ot_path = raw_data['u_tr_time']

idx_list = ['user_id','item_id','behavior_type','user_geohash','item_category','time']

# TODO 先抽正例，然后列一个禁止list，抽出来的直接存起来吧
def get_positive_item(paths):
    "get the positive item and the u-i dict."

    pi_list = []
    ban_list = []

    infile = open(paths['u_te_time'],'rb')
    
    for idx, row in enumerate(DictReader(infile)):
        
        if row['behavior_type'] == '4':
            if row['user_id'] not in ban_list:
                ban_list.append((row['user_id'],row['item_id']))
                tmp = ','.join([row[key] for key in idx_list])
                pi_list.append(tmp)
    infile.close() 

    hold_num = 24000

    counts = 0
    ng78_list = []

    infile = open(paths['u_te_time'],'rb')
    for idx, row in enumerate(DictReader(infile)):
        if row['behavior_type'] != '4':
            if (row['user_id'],row['item_id']) not in ban_list:
                if random() > 0.95 and counts < 24000:
                    tmp = ','.join([row[key] for key in idx_list])
                    ng78_list.append(tmp)
                    counts += 1
        if counts >= hold_num:
            print idx
            break
    infile.close()

    counts = 0
    ng_list = []

    infile = open(paths['u_tr_time'],'rb')
    for idx, row in enumerate(DictReader(infile)):
        if row['behavior_type'] != '4':
            if (row['user_id'],row['item_id']) not in ban_list:
                if random() > 0.98 and counts < 2400:
                    tmp = ','.join([row[key] for key in idx_list])
                    ng_list.append(tmp)
                    counts += 1
        if counts >= hold_num:
            print idx
            break
    

if __name__ == "__main__":
    get_positive_item(raw_data)
