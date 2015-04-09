#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :gen_dataset.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
'''
    利用文件，获得相应大小的dataset，剔除就好了，不用自己随机来
'''
import sys
sys.path.append('..')

import logging
from csv import DictReader,writer
from optparse import OptionParser
from util.get_item import get_raw_conf
from random import random

raw_data = get_raw_conf()

idx_list = ['user_id','item_id','behavior_type','user_geohash','item_category','time']

# TODO 获得正例u_i，同时将正例写到tmp文件中去
def adjust_dataset(data_path,new_path):
    ''' get the positive instance and the ban_list'''
    #获得了正例集合，u-i-t
    ban_dict = {}
    infile = open(data_path,'rb')
    for row in DictReader(infile):
        if row['behavior_type'] =='4':
            if (row['user_id'],row['item_id']) in ban_dict:
                ban_dict[(row['user_id'],row['item_id'])].append(row['time'])
            else:
                ban_dict[(row['user_id'],row['item_id'])] = [row['time']]
    print 'total positive instances are : ',len(ban_dict)
    infile.close()

    ifile = open(data_path,'rb')
    ofile = open(new_path,'wb')
    rand_w = writer(ofile)
    rand_w.writerow(idx_list)

    for idx,row in enumerate(DictReader(ifile)):
        tmp = [row[key] for key in idx_list]
        if (row['user_id'],row['item_id']) in ban_dict and row['time'] in ban_dict[(row['user_id'],row['item_id'])] and row['behavior_type'] != '4':
            pass
        else:
            if row['behavior_type'] == '4':
                rand_w.writerow(tmp)
            else:
                if random() < 0.05:
                    rand_w.writerow(tmp)
        if (idx+1) % 10000 == 0:
            print idx+1
    ifile.close()
    ofile.close()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-d','--data',dest='data',help='选择抽取的数据集')

    (options,args) = parser.parse_args()
    
    if options.data == 'train':
        adjust_dataset(raw_data['u_tr_time'],raw_data['n_tr_time'])
    elif options.data == 'test':
        adjust_dataset(raw_data['u_te_time'],raw_data['n_te_time'])
    else:
        print 'error'
        sys.exit(1)

