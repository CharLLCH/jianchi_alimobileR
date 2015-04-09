#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :adjust_data.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
'''
    调整训练数据

max_tr_num = 400000

infile = open('../data/u_tr_rand_70.csv','rb')
outfile = open('../data/u_tr_rand.csv','wb')

idx = 0
while(idx <= max_tr_num):
    line = infile.readline()
    outfile.write(line)
    idx += 1

infile.close()
outfile.close()

print idx
import csv

infile = open('../data/pred129.csv','rb')
outfile = open('../data/test_set.csv','wb')

u_i_dict = {}
count = 0
idx = 0
for line in infile.readlines():
    its = line.strip().split(',')
    if (its[0],its[1]) not in u_i_dict:
        u_i_dict[(its[0],its[1])] = 1
        outfile.write(line)
        idx += 1 
    count += 1

infile.close()
outfile.close()

print idx,count
'''
import sys
sys.path.append('..')

import logging
import datetime
from csv import DictReader,writer
from util.get_item import get_raw_conf

raw_data = get_raw_conf()

idx_list = ['user_id','item_id','behavior_type','user_geohash','item_category','time']

def adjust_new_tr_days():
    infile = open(raw_data['n_tr_time'],'rb')
    target_day = datetime.date(2014,12,15)
    outfile = open(raw_data['n_tr_days'],'wb')
    ntd = writer(outfile)
    ntd.writerow(idx_list)

    for idx,row in enumerate(DictReader(infile)):
        tmp = [row[key] for key in idx_list]
        tmp_dts = row['time'].split(' ')[0]
        tmp_dt = tmp_dts.split('-')
        ddis = (datetime.date(int(tmp_dt[0]),int(tmp_dt[1]),int(tmp_dt[2])) - target_day).days
        if ddis >= 0:
            ntd.writerow(tmp)
        if idx % 100000 == 0:
            print idx

    outfile.close()
    infile.close()

if __name__ == "__main__":
    adjust_new_tr_days()
