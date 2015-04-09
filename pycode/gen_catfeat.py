#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :gen_catfeat.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
import sys
sys.path.append('..')

from csv import DictReader
from optparse import OptionParser
import pickle
import datetime
from util.get_item import get_raw_conf

raw_data = get_raw_conf()

Max_day = 22
u_c_dict = {}

infile = open(raw_data['usr_train_path'],'rb')

for idx, row in enumerate(DictReader(infile)):
    flags = False
    # TODO 第一次遇到这个user，全加
    if row['user_id'] not in u_c_dict:
        u_c_dict[row['user_id']] = {}
        tmp_list = [0] * 4
        tmp_list[int(row['behavior_type'])-1] = 1
        u_c_dict[row['user_id']][row['item_category']] = {}
        u_c_dict[row['user_id']][row['item_category']][row['time'][0:10]] = tmp_list
        flags = True
    else:
        # TODO 第一次遇到这个category，在这个user内，全加
        if row['item_category'] not in u_c_dict[row['user_id']]:
            tmp_list = [0] * 4
            tmp_list[int(row['behavior_type'])-1] = 1
            u_c_dict[row['user_id']][row['item_category']] = {}
            u_c_dict[row['user_id']][row['item_category']][row['time'][0:10]] = tmp_list
            flags = True
        else:
            # TODO 第一次遇到这一天，在category下，全加
            if row['time'][0:10] not in u_c_dict[row['user_id']][row['item_category']]:
                tmp_list = [0] * 4
                tmp_list[int(row['behavior_type'])-1] = 1
                u_c_dict[row['user_id']][row['item_category']][row['time'][0:10]] = tmp_list
                flags = True
            # TODO 有这个用户，有这个类别，这一天还有过记录，增加一个相应的就好了
            else:
                u_c_dict[row['user_id']][row['item_category']][row['time'][0:10]][int(row['behavior_type'])-1] += 1
                flags = True
    if flags == False:
        print 'here some not add..'

print 'Dict Ready..'

def get_dis(t,d):
    tmp_t = datetime.date(int(t[0:4]),int(t[5:7]),int(t[8:10]))
    tmp_d = datetime.date(int(d[0:4]),int(d[5:7]),int(d[8:10]))
    tmp_v = (tmp_t - tmp_d).days
    return tmp_v

def get_one_cat_feat(u_id,i_cat,ui_dt):
    '''获得这个用户在这一天在这个dis内的，对于这个cat的op'''
    feat_list = [0] * 4 * Max_day
    tar_dt = ui_dt[0:10]
    for days in u_c_dict[u_id][i_cat]:
        dis = get_dis(tar_dt,days)
        if dis > 0 and dis <= Max_day:
            #统计出来
            for i in range(4):
                feat_list[(dis-1)*4+i] += u_c_dict[u_id][i_cat][days][i]

    tmp_str = ''
    for key in feat_list:
        tmp_str += ',%s'%(key)
    tmp_str += '\n'
    return tmp_str


# TODO 已经得到feats，现在根据原来文件中的u_id,item_id,i_cat,date来获取对应的catfeat
# 然后将两个合并成一个文件，然后作新的特征
# 原来的f1,f2....,fn\n 现在把\n去了，接 ,c1,c2,c3...,cm就好

def merge_feat(o_data,o_feat,m_feat):
    odfile = open(o_data,'rb')
    offile = open(o_feat,'rb')
    offile.readline()
    mffile = open(m_feat,'wb')
    mffile.write('with category\n')

    for idx,row in enumerate(DictReader(odfile)):
        #get the uid iid uidt
        tmp_feat = offile.readline().strip()
        tmp_feat += get_one_cat_feat(row['user_id'],row['item_category'],row['time'])
        mffile.write(tmp_feat)
        if idx % 50000 == 0:
            print idx

    odfile.close()
    offile.close()
    mffile.close()

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-d','--data',dest='data',help='train , test or pred')

    (options,args) = parser.parse_args()

    if options.data == 'train':
        print 'start to merge the training set'
        merge_feat(raw_data['n_tr_time'],raw_data['train_dir'],raw_data['tr_cat_dir'])
    elif options.data == 'test':
        print 'start to merge the testing set'
        merge_feat(raw_data['n_te_time'],raw_data['test_dir'],raw_data['te_cat_dir'])
    elif options.data == 'pred':
        print 'start to merge the preding set'
        merge_feat(raw_data['test_set'],raw_data['pred_dir'],raw_data['pr_cat_dir'])
    else:
        print 'Something wrong in options'
        sys.exit(1)
