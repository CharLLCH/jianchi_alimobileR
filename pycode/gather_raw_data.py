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
    遍历所有的数据，按照用户id将所有操作存到字典中去
'''

import sys
sys.path.append("..")

from util.read_conf import config

from csv import DictReader
from datetime import datetime
import pickle

raw_data = config('../conf/raw_data.conf')
usr_path = raw_data['usr_train_path']

# TODO transform the date time format.
def date_transform(item_time):
    "trans the time to 1-7 & 1-24"
    #feat[0:4]=Y,[5:7]=M,[8,10]=D,[-2:]=H
    time_feat = datetime(int(item_time[0:4]),int(item_time[5:7]),int(item_time[8:10]))
    hour_feat = item_time[-2:]
    
    week_feat = time_feat.strftime("%A")

    tmp = week_feat+'-'+hour_feat
    return tmp

# TODO get the target product that some one buy or add into the car.
def get_target_product(tar_path):
    "traverse the list, and find the target list of the product id."

    print 'open the file of ',tar_path
    infile = open(tar_path,'rb')

    ui_dict = {}
    counts = 0
    
    for idx, row in enumerate(DictReader(infile)):
        
        if row['behavior_type'] != '1':
            counts += 1
            if row['user_id'] in ui_dict:
                # 是否该将其他的信息都加上呢，如果一个人在不同时间地点买过同一个id的商品两次得区分开啊
                date_feat = date_transform(row['time'])
                tmp = ',' + row['item_id'] + '-' + row['behavior_type'] + '-' + date_feat
                ui_dict[row['user_id']] += tmp
            else:
                tmp = row['item_id'] + '-' + row['behavior_type'] + '-' + date_transform(row['time'])
                ui_dict[row['user_id']] = tmp

        if (idx+1) % 1000000 == 0:
            print (idx+1)/1000000,'m'

    #将购买信息
    outfile = open(raw_data['usr_pur_path'],'wb')
    pickle.dump(ui_dict,outfile,True)
    print 'get the puchase items.'

if __name__ == "__main__":
    get_target_product(usr_path)
