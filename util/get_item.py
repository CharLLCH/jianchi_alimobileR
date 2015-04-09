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
import sys

rawconf_dir = '../conf/raw_data.conf'
dbconf_dir = '../conf/db.conf'

raw_conf = config(rawconf_dir)
db_conf = config(dbconf_dir)

def get_raw_conf():
    return raw_conf

def get_db_conf():
    return db_conf

def get_one_item(op,data_path):
    infile = open(data_path,'rb')
    
    for idx,row in enumerate(DictReader(infile)):
        s_item = item(row['user_id'],row['item_id'],row['behavior_type'],row['item_category'],row['time'],row['user_geohash'])
        if op == 'train':
            yield s_item
        elif op == 'dict':
            yield row
        else:
            yield [s_item,row]

def get_item(dt='total',op="train"):
    if dt == 'total':
        f = open(raw_conf['user_train_path'])
    elif dt == 'train':
        f = open(raw_conf['n_tr_time'])
    elif dt == 'test':
        f = open(raw_conf['n_te_time'])
    elif dt == 'pred':
        f = open(raw_conf['test_set'])
    else:
        print "no such file dir."
        sys.exit(1)

    for idx,row in enumerate(DictReader(f)):
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
