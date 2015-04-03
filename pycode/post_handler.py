#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :post_handler.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
import sys
sys.path.append('..')

import datetime
import time
import logging
import mysql.connector
from util.get_item import get_db_conf

db_conf = get_db_conf()


try:
    conn = mysql.connector.connect(host=db_conf['host'],user=db_conf['user'],passwd=db_conf['passwd'])
except Exception as err:
    logging.error(err)

cur = conn.cursor()
cur.execute('use %s'%(db_conf['db_name']))

infile = open('../data/tianchi_mobile_recommendation_predict.csv','rb')
outfile = open('../tianchi_mobile_recommendation_predict.csv','wb')

count = 0
idx = 0

cat_dict = {}
catfile = open('../data/item_train.csv','rb')
for cat_line in catfile.readlines():
    tmp_list = cat_line.strip().split(',')
    if tmp_list[0] not in cat_dict:
        cat_dict[tmp_list[0]] = tmp_list[2]
catfile.close()
print 'get the item-cat dict : ',len(cat_dict)

for line in infile.readlines():
    count += 1
    tmp_list = line.strip().split(',')
    u_id = tmp_list[0]
    i_id = tmp_list[1]
    target_date = datetime.date(2014,12,19)
    #sql_cat = 'select distinct icat from user_train where item=\"%s\"'%(i_id)
    #cur.execute(sql_cat)
    #cat_result = cur.fetchall()
    #i_cat = cat_result[0]
    if i_id in cat_dict:
        i_cat = cat_dict[i_id]
    else:
        pass
    sql_uc = 'select behavior,ubdate from user_train where user=\"%s\" and icat=\"%s\"'%(u_id,i_cat)
    cur.execute(sql_uc)
    uc_result = cur.fetchall()
    flags = False
    for uc in uc_result:
        day_dis = (target_date - uc[1]).days
        if day_dis <= 7:
            if uc[0] == 4:
                flags = False
                break
            elif uc[0] == 2 or uc[0] == 3:
                flags = True
            else:
                pass
    if flags:
        idx += 1
        if idx % 100 == 0:
            print idx
        outfile.write(line)

outfile.close()
infile.close()
print idx,count
