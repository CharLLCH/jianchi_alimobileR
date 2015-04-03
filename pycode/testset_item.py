#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :gen_testset.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

'''
    based on user and the P's item to generate the D' to predict
'''

import sys
sys.path.append('..')

import mysql.connector
import logging,time
import datetime
from csv import DictReader

from util.get_item import get_db_conf,get_raw_conf

def get_testset_item():
    raw_conf = get_raw_conf()
    db_conf = get_db_conf()
    
    print "start to connect the db.."
    try:
        conn = mysql.connector.connect(host=db_conf['host'],user=db_conf['user'],passwd=db_conf['passwd'])
    except Exception as err:
        logging.error(err)
    
    cur = conn.cursor()
    cur.execute('use %s'%(db_conf['db_name']))
    
    print 'start to search the users..'
    sql_str = 'select distinct user from user_train'
    cur.execute(sql_str)
    
    user_list = cur.fetchall()
    
    dates = datetime.date(2014,12,19)
    
    infile = open('../data/item_train.csv','rb')
    
    item_dict = {}

    print 'start to get the items.'
    
    for idx,row in enumerate(DictReader(infile)):
        if row['item_id'] not in item_dict:
            item_dict[row['item_id']] = row['item_category']
        else:
            print row['item_id']
    
    # TODO user_list 和 item_dict 可以存起来的

    print 'got the users items'

    for user in user_list:
        for item in item_dict:
            yield [user,item,item_dict[item]]
