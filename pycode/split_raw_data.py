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
    # 重写split函数，不是路径定死的，传入数据，获得ban_list等
    # 对于同样类型的数据集，直接可使用
'''

import sys
sys.path.append('..')

from csv import DictReader,writer
from random import random
from util.get_item import get_raw_conf
import pickle
import logging

idx_list = ['user_id','item_id','behavior_type','user_geohash','item_category','time']

# TODO 获得正例items和ban_list
def get_posban_list(data_path,pi_path):
    ''' get the positive items and the ban_list'''
    pi_list = []
    ban_list = []

    infile = open(data_path,'rb')
    for idx, row in enumerate(DictReader(infile)):
        if row['behavior_type'] == '4':
            if (row['user_id'],row['item_id']) not in ban_list:
                ban_list.append((row['user_id'],row['item_id']))
                pi_list.append([row[key] for key in idx_list])
    print 'total positive items are : ',len(pi_list)
    infile.close()

    pi_file = open(pi_path,'wb')
    pickle.dump(pi_list,pi_file,True)

    return ban_list

# TODO 根据ban_list和raw数据获得负例list
def get_nag_list(data_path,ng_path,ban_list,max_num):
    '''get the nagetive items'''
    ng_list = []
    num_ng = 0

    infile = open(data_path,'rb')
    for idx, row in enumerate(DictReader(infile)):
        if row['behavior_type'] == '1':
            if (row['user_id'],row['item_id']) not in ban_list:
                if random() < 0.9 and num_ng < max_num:
                    ng_list.append([row[key] for key in idx_list])
                    num_ng += 1
                    if num_ng % 1000 == 0:
                        print 'get num : ',num_ng,'nagtive items'
        if num_ng >= max_num:
            print 'sampling at the index : ',idx
            break
    infile.close()

    ng_file = open(ng_path,'wb')
    pickle.dump(ng_list,ng_file,True)

# TODO 根据两个数据集，将正负例合并到一起
def merge_pos_ng(pi_path,ng_path,final_path):
    '''merge the positive items and the nagetive items'''
    pi_list = pickle.load(open(pi_path,'rb'))
    ng_list = pickle.load(open(ng_path,'rb'))

    outfile = open(final_path,'wb')
    rand_writer = writer(outfile)
    rand_writer.writerow(idx_list)

    idx_pos = 0
    idx_nag = 0
    n_pos = len(pi_list)
    n_nag = len(ng_list)

    while(1):
        rand = random()
        if idx_pos < n_pos:
            if rand < 0.01:
                rand_writer.writerow(pi_list[idx_pos])
                idx_pos += 1
            else:
                if idx_nag < n_nag:
                    rand_writer.writerow(ng_list[idx_nag])
                    idx_nag += 1
                else:
                    rand_writer.writerow(pi_list[idx_pos])
                    idx_pos += 1
        else:
            if idx_nag < n_nag:
                rand_writer.writerow(ng_list[idx_nag])
                idx_nag += 1
            else:
                break

    print 'total split_items :',idx_nag+idx_pos,'pos_items:',idx_pos,'nag_items:',idx_nag

    outfile.close()

if __name__ == "__main__":

    raw_data = get_raw_conf()
    pi_path = '../result/pi_tmp.pkl'
    ng_path = '../result/ng_tmp.pkl'

    opt = sys.argv[1]
    if opt not in ['train','test']:
        logging.error('option is wrong.')
        sys.exit(1)
    elif opt == 'train':
        # split the train dataset.
        data_path = raw_data['u_tr_time']
        #out_path = raw_data['u_tr_rand']
        out_path = '../data/new_tr_rand.csv'
        max_num = 9900000
    else:
        # split the test dataset.
        data_path = raw_data['u_te_time']
        out_path = raw_data['u_te_rand']
        max_num = 12000

    ban_list = get_posban_list(data_path,pi_path)
    get_nag_list(data_path,ng_path,ban_list,max_num)
    merge_pos_ng(pi_path,ng_path,out_path)
