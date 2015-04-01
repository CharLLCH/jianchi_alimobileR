#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :adjust_data.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

'''
    调整训练数据
'''

max_tr_num = 500000

infile = open('../data/u_tr_rand_70.csv','rb')
outfile = open('../data/u_tr_rand_ad.csv','wb')

idx = 0
while(idx <= max_tr_num):
    line = infile.readline()
    outfile.write(line)
    idx += 1

infile.close()
outfile.close()

print idx
