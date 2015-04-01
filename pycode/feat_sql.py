#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :feat_sql.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
'''
    #sql_str = "CREATE table user_train (user char(13),item char(13), behavior tinyint,ugeo char(10),icat char(10),ubdate date,ubhour tinyint,week_f,hour_f, index idx1(user(8)),index idx2(item(8)),index idx3(ugeo),index idx4(icat),index idx5(ubdate))"
    #feature: uid+iid: x x x x ...
    #用户-商品的操作 => 向user+item:[feats]走， => 现在有所有的操作记录，然后有当前的数据集[不是该根据平衡过的数据集么！？]
    #这里对于每条记录，都是同等地寻找其之前N天的数据，从而达到抽取的feat是同样的，但是对于不同时间的同样用户和商品，feat是不同的
    #这里就是根据想找的方面的feat，找到所有数据，然后count具体的featvalue
'''

import sys
sys.path.append('..')

import mysql.connector
import logging,time
import datetime
import itertools
import csv

from util.item import item
from util.get_item import get_db_conf,get_one_item,get_raw_conf

raw_conf = get_raw_conf()
db_conf = get_db_conf()

try:
    conn = mysql.connector.connect(host=db_conf['host'],user=db_conf['user'],passwd=db_conf['passwd'])
except Exception as err:
    logging.error(err)

cur = conn.cursor()
cur.execute("use %s"%(db_conf['db_name']))

pre_day = 15
item_cat_num = 4


def date_trans(date_time):
    date_feat = date_time.split('-')
    return datetime.date(int(date_feat[0]),int(date_feat[1]),int(date_feat[2]))

# TODO 根据两个全局量创建u-i类的特征字典
def construct_feat_dict():
    '''根据要向前看的天数和商品最大种类进行创建feat字典'''
    day_feat = ['d%s'%(i) for i in range(1,pre_day)]
    beh_feat = ['b%s'%(i) for i in range(1,item_cat_num+1)]

    # 笛卡尔积，按照一个数组有序的
    com_feat = list(itertools.product(day_feat,beh_feat))
    com_feat = ['%s_%s'%(i,j) for i,j in com_feat]

    # 根据set(com_feat)中的值作key，value默认0，创建字典
    feats = dict.fromkeys(set(com_feat),0)
    return feats

# TODO 对于每个时间的u-i对，进行对应特征的抽取，一天内的对是等同的
def get_user_item(u_id,i_id,date_time,flags):
    '''根据这两个id，和时间，抽取相应的所有的特征'''

    if flags == 'ui':
        sql_str = 'select behavior,ubdate from user_train where user=\"%s\" and item=\"%s\"'%(u_id,i_id)
    elif flags == 'i':
        sql_str = 'select behavior,ubdate from user_train where item=\"%s\"'%(i_id)
    else:
        sql_str = 'select behavior,ubdate from user_train where user=\"%s\"'%(u_id)

    cur.execute(sql_str)
    result = cur.fetchall()

    feat_dict = construct_feat_dict()

    dates = date_trans(date_time)

    for single_re in result:
        # s[0]-behavior s[1]-userbehavior-date
        day_dis = (dates - single_re[1]).days
        user_beh = single_re[0]

        feat_str = 'd%s_b%s'%(day_dis,user_beh)
        if feat_str in feat_dict:
            feat_dict[feat_str] += 1

    feat_dict_flag = {'%s_%s'%(flags,key):feat_dict[key] for key in feat_dict}
    return feat_dict_flag


# TODO 构建出来feat的维度
def get_fields():
    fields = ['b_type','i_cat']
    tmp_dict = construct_feat_dict()
    for key in tmp_dict:
        fields.append('ui_%s'%(key))
    for key in tmp_dict:
        fields.append('i_%s'%(key))

    return fields


# TODO 合并两个featdict
def merge_feats(feat_path):
    '''暂时将两个dict合并成一个'''
    # 先将fields确定下来
    fields = get_fields()
    
    out_file = open(feat_path,'w')
    writer = csv.DictWriter(out_file,fields)

    # 每次得到一个item

    click_file = open(raw_conf['f_tr_rand_click'],'w')

    items = get_one_item()
    count = 0

    for item in items:
        ui_dict = get_user_item(item.user_id,item.item_id,item.date,'ui')
        i_dict = get_user_item(item.user_id,item.item_id,item.date,'i')
        tmp_dict = dict(ui_dict,**i_dict)
        r_dict = item.get_field_dict()
        final_dict = dict(tmp_dict,**r_dict)

        writer.writerow(final_dict)
        count += 1

        if item.behavior_type == '4':
            tmp = '1\n'
        else:
            tmp = '0\n'
        click_file.write(tmp)

        
        if count % 1000 == 0:
            print count

    out_file.close()
    click_file.close()


def main():
    '''e..'''
    merge_feats(raw_conf['f_tr_rand'])


if __name__ == "__main__":
    main()
