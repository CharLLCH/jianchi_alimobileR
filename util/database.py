#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :database.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

import sys

import mysql.connector
import logging
from .read_conf import config
import cPickle as pickle
import random

conf = config('../conf/raw_data.conf')

class mysql_db:
    def __init__(self,host,port,user,passwd):
        self.count = 0
        try:
            self.conn = mysql.connector.connect(host=host,user=user,passwd=passwd,port=port)
        except Exception as err:
            logging.error(err)

    def create_db(self,db_name):
        try:
            cur = self.conn.cursor()
            sql_str = "CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8"%(db_name)
            cur.execute(sql_str)
            self.conn.commit()
        except Exception as err:
            logging.error(err)

    def drop_db(self,db_name):
        try:
            cur = self.conn.cursor()
            sql_str = "drop database if exists %s;"%(db_name)
            cur.execute(sql_str)
            self.conn.commit()
        except Exception as err:
            logging.error(err)

    def insert_sql(self,sql_str,db_name,commit_num = 1):
        try:
            self.count += 1
            cur = self.conn.cursor()
            cur.execute("use %s"%(db_name))
            cur.execute(sql_str)
            if self.count % commit_num == 0:
                self.conn.commit()
                self.count = 0
        except Exception as err:
            logging.error(err)

    def select_sql(self,sql_str,db_name):
        self.select_count += 1
        cur = self.conn.cursor()

        cur.execute("use %s"%(db_name))
        cur.execute(sql_str)

        result = cur.fetchall()
        return result
