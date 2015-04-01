#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :get_item.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

'''
    数据、配置的载入
'''

from csv import DictReader
from read_conf import config
from item import item
from optparse import OptionParser
import unittest
import pickle

rawconf_dir = '../conf/raw_data.conf'
dbconf_dir = '../conf/db.conf'
raw_conf = config(rawconf_dir)
db_conf = config(dbconf_dir)

def get_raw_conf():
    return raw_conf

def get_db_conf():
    return db_conf

def get_one_item(op='train'):
    infile = open(raw_conf['u_tr_rand_ad'],'rb')
    #infile = open(raw_conf['u_te_rand_8'],'rb')
    
    for idx,row in enumerate(DictReader(infile)):
        s_item = item(row['user_id'],row['item_id'],row['behavior_type'],row['item_category'],row['time'],row['user_geohash'])
        if op == 'train':
            yield s_item
        elif op == 'dict':
            yield row
        else:
            yield [s_item,row]

if __name__ == "__main__":
    items = get_one_item()
    for s_item in items:
        print s_item.sql_str()
