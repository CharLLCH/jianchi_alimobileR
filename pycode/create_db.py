#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :create_db.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

# 将所有输出数据或者配置放到一个文件里还是一个不错的选择的
# 这样就不用在各个文件中添加read_conf了

import sys
sys.path.append('..')
import mysql.connector
import logging

from util.item import item
from util.get_item import get_db_conf,get_one_item,get_raw_conf

raw_conf = get_raw_conf()
data_path = raw_conf['u_tr_time']
dbconf = get_db_conf()

host = dbconf['host']
user = dbconf['user']
passwd = dbconf['passwd']

if passwd == 'null':
    passwd = ""

conn = mysql.connector.connect(host=host,user=user,passwd=passwd)

def create():

    cur = conn.cursor()

    sql_str = "CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8"%("alibaba")
    cur.execute(sql_str)

    sql_str = "use alibaba"
    cur.execute(sql_str)

    sql_str = "CREATE table user_train (user char(13),item char(13), behavior tinyint,ugeo char(10),icat char(10),ubdate date,ubhour tinyint,weekend char(8),time_f char(1), index idx1(user(8)),index idx2(item(8)),index idx3(ugeo),index idx4(icat),index idx5(ubdate))"
    cur.execute(sql_str)
    
    conn.commit()

    items = get_one_item('train',data_path)
    count = 0

    for s_item in items:
        cur.execute(s_item.sql_str())

        count += 1
        if count % 10000 == 0:
            print 'store the items',count / 10000.0,'W'
            conn.commit()

    conn.commit()

def delete_db():
    cur = conn.cursor()
    cur.execute("drop database if exists alibaba")
    conn.commit()

if __name__ == "__main__":
    opt = sys.argv[1]
    if opt not in ['create','delete']:
        logging.error('option not define..')
        sys.exit(1)
    elif opt == 'create':
        create()
    else:
        delete_db()
