#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :still_bad_coding.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

import sys
sys.path.append('..')

import mysql.connector
import logging
import datetime
import itertools
import csv

from util.item import item
from util.get_item import get_db_conf,get_one_item,get_raw_conf

# 获得数据文件和数据库相关的配置信息
raw_conf = get_raw_conf()
db_conf = get_db_conf()

# TODO 打开数据库
try:
    conn = mysql.connector.connect(host=db_conf['host'], user=db_conf['user'],passwd=db_conf['passwd'])
except Exception as err:
    logging.error(err)

# TODO 切换数据库
cur = conn.cursor()
cur.execute('use %s'%(db_conf['db_name']))


def trans_date(date_str):
    '''TODO 字符串转换成datetime形式，方便加减'''
    tmp = [int(i) for i in date_str.split('-')]
    return datetime.date(tmp[0],tmp[1],tmp[2])

'''
    # 对于数据集，每次都是一条数据，购买与否确定了是否是正例
    # 同时，包含user item的数据，同时behavior不能包含
    # 那就只包含一个当前类别，地理位置信息，星期和时间段
    # 不能都是数字型，类别变量或者字符串也需要处理下了
    # 所以item和get_item都需要调整
    # 最后，不合成一个dict了，我需要分组！
    # so 自带特征一组，各类统计各自组
    # 数字型，user，item总览，1234统计的生气也给你弄成cat！
    # 购物和items23的可以视作cat吧
    # 先去改进输入！
'''

PRE_DAYS = 7
G_fields = []
#PRE_DAYS = 15
# TODO pre_days 总览，前3天的23，要来就来个全的打包件么！

def what_the_hell_feat(idx,flags):
    '''TODO get what I want !'''
    #TODO line info
    u_id = idx.user_id
    i_id = idx.item_id
    i_cat = idx.item_category
    u_geo = idx.user_geohash
    week = idx.week_f
    date = idx.date
    hour = idx.hour_f

    if flags == 'u_i':
        # 找到这个用户和这个商品在这两天的关系
        sql_str = 'select behavior,ubdate from user_train where user=\"%s\" and item=\"%s\"'%(u_id,i_id)
    elif flags == 'u':
        sql_str = 'select behavior,ubdate from user_train where user=\"%s\"'%(u_id)
    elif flags == 'i':
        sql_str = 'select behavior,ubdate from user_train where item=\"%s\"'%(i_id)
    else:
        sql_str = 'select behavior,ubdate from user_train where icat=\"%s\"'%(i_cat)

    cur.execute(sql_str)
    if cur != None:
        sql_result = cur.fetchall()

        tar_date = trans_date(date)
        feat_dict = construct_feat_fields()

        for sql_item in sql_result:
            ub = sql_item[0]
            ubd = sql_item[1]
            day_dis = (tar_date - ubd).days
            if day_dis > 7:
                pass
            elif day_dis >= 1:

                more_str = 'd%s_be_%s'%(day_dis,ub)
                if more_str in feat_dict:
                    feat_dict[more_str] += 1

                if day_dis <= 3:
                    feat_str = 'in_3d_be_%s'%(ub)
                    feat_dict[feat_str] += 1

                if day_dis <= 7:
                    feat_str = 'in_7d_be_%s'%(ub)
                    feat_dict[feat_str] += 1
            else:
                pass

    feat_dict_flag = {'%s_%s'%(flags,key):feat_dict[key] for key in feat_dict}

    return feat_dict_flag

def get_fields(idict):
    fields = []
    for key in idict:
        fields.append(key)
    tmp_dict = construct_feat_dict()
    for key in tmp_dict:
        fields.append('ui_%s'%(key))
    for key in tmp_dict:
        fields.append('i_%s'%(key))
    for key in tmp_dict:
        fields.append('u_%s'%(key))
    for key in tmp_dict:
        fields.append('c_%s'%(key))

    return fields

def construct_feat_fields():
    '''产生存放的域'''
    day_feat = ['in_%sd'%(i) for i in [3,7]]
    for i in range(PRE_DAYS):
        day_feat.append('d%s'%(i))
    beh_feat = ['be_%s'%(i) for i in range(1,5)]

    com_feat = list(itertools.product(day_feat,beh_feat))
    com_feat = ['%s_%s'%(i,j) for i,j in com_feat]

    return dict.fromkeys(set(com_feat),0)
    
    
def merge_feat(feat_path,data_path):
    '''TODO save the feat_line(in what some format)'''
    # 写feat
    out_file = open(feat_path,'wb')

    truths = get_one_item('train',data_path)

    count = 0

    for idx in truths:
        # one by one
        self_feat = idx.new_feat()
        u_i_feat = what_the_hell_feat(idx,'u_i')
        u_feat = what_the_hell_feat(idx,'u')
        i_feat = what_the_hell_feat(idx,'i')
        c_feat = what_the_hell_feat(idx,'c')
        # based on what tools write the feat_dict
        #label [importance tag]|namespace feats feats |namespace feats ..
        
        str_line = ''
        if idx.behavior_type == '4':
            str_line += '1 1.5 '
        else:
            str_line += '-1 0.5 '
        str_line += '%s-%s'%(idx.user_id,idx.item_id)
        str_line += gen_str(u_i_feat,'u_i')
        str_line += gen_str(u_feat,'y_h')
        str_line += gen_str(i_feat,'s_p')
        str_line += gen_str(c_feat,'i_c')
        str_line += gen_str(self_feat,'f_s')
        str_line += '\n'
        count += 1
        out_file.write(str_line)
        if count % 10 == 0:
            print 'No. --:-->',count,'  ',data_path,'==:==> ', str_line

    out_file.close()


def gen_str(fdict,flags):
    tmp_str = '|%s '%(flags)
    for key in fdict:
        tmp_str += '%s '%(fdict[key])
    return tmp_str

def main():
    '''TODO set the paramters'''
    merge_feat('../vwdatatest/vw_testset.csv','../data/u_te_time.csv')
    merge_feat('../vwdatatest/vw_trainset.csv','../data/u_tr_time.csv')
    
if __name__ == "__main__":
    main()
