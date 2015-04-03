#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :submit_list.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

import sys
sys.path.append('..')

from util.get_item import get_raw_conf

raw_data = get_raw_conf()

test_set = raw_data['test_set']
click_set = raw_data['test_pur']

outfile = open('../result/tianchi_mobile_recommendation_predict.csv','wb')
outfile.write('user_id,item_id\n')

infile_t = open(test_set,'rb')
infile_c = open(click_set,'rb')

for line in infile_c.readlines():
    ui_line = infile_t.readline()
    if line.strip() == '1':
        ui_list = ui_line.strip().split(',')
        tmp = '%s,%s\n'%(ui_list[0],ui_list[1])
        outfile.write(tmp)

infile_t.close()
infile_c.close()
outfile.close()
