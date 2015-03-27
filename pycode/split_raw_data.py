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
    counts = 0
    ng_list = []

    infile = open(paths['u_tr_time'],'rb')
    for idx, row in enumerate(DictReader(infile)):
        if row['behavior_type'] != '4':
            if (row['user_id'],row['item_id']) not in ban_list:
                if random() > 0.98 and counts < 24000:
                    tmp = ','.join([row[key] for key in idx_list])
                    ng_list.append(tmp)
                    counts += 1
        if counts >= hold_num:
            print idx
            break
    if counts < hold_num:
        print 'still not enough.'
    infile.close()

    #infile_tr = open(paths['u_tr_time'],'rb')
    #for idx, row in enumerate(DictReader(infile_tr)):
    #    if row['behavior_type'] != '4':
    #        if (row['user_id'],row['item_id']) not in ban_list:
    #            if random() > 0.9 and counts < 2400:
    #                tmp = ','.join([row[key] for key in idx_list])
    #                ng_list.append(tmp)
    #                counts += 1
    #    if counts >= hold_num:
    #        print idx
    #        break
    #infile_tr.close()
'''

'''
    非17-18的，不是4的，且不在17-18-4的u和i的，随便抽2w4
    17-18的，不是4且不和17-18-4对应的u和i冲突的，随便抽2w4
    正例就17 18的所有的 u-i-4
'''
import sys
sys.path.append('..')

from csv import DictReader,writer
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
                #tmp = ','.join([row[key] for key in idx_list])
                tmp = [row[key] for key in idx_list]
                pi_list.append(tmp)
    infile.close() 
    hold_num = 12000
    counts = 0
    ng78_list = []
    infile = open(paths['u_te_time'],'rb')
    for idx, row in enumerate(DictReader(infile)):
        if row['behavior_type'] == '1':
            if (row['user_id'],row['item_id']) not in ban_list:
                if random() > 0.96 and counts < 24000:
                    #tmp = ','.join([row[key] for key in idx_list])
                    tmp = [row[key] for key in idx_list]
                    ng78_list.append(tmp)
                    counts += 1
        if counts >= hold_num:
            print idx
            break
    infile.close()
    outfile_78 = open(paths['u_te_rand_8'],'wb')
    rand_writer_78 = writer(outfile_78)
    
    rand_writer_78.writerow(idx_list)

    num_positive = len(pi_list)
    num_nagetive = len(ng78_list)

    print len(pi_list),len(ng78_list)

    idx_pos = 0
    idx_nag = 0

    while(1):
        rand = random()
        if idx_pos < num_positive:
            if rand < 0.25:
                # insert the pos_item
                #rand_writer.writerow(pi_list[idx_pos])
                rand_writer_78.writerow(pi_list[idx_pos])
                idx_pos += 1
            else:
                if idx_nag < num_nagetive:
                    #insert the nagetive_item
                    #rand_writer.writerow(ng_list[idx_nag])
                    rand_writer_78.writerow(ng78_list[idx_nag])
                    idx_nag += 1
                else:
                    #insert the pos_item
                    #rand_writer.writerow(pi_list[idx_pos])
                    rand_writer_78.writerow(pi_list[idx_pos])
                    idx_pos += 1
        else:
            if idx_nag < num_nagetive:
                #insert nag_item
                #rand_writer.writerow(ng_list[idx_nag])
                rand_writer_78.writerow(ng78_list[idx_nag])
                idx_nag += 1
            else:
                break

    outfile_78.close()
    #outfile.close()
    
    
if __name__ == "__main__":
    get_positive_item(raw_data)
