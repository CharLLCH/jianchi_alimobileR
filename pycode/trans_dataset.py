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

max_tr_num = 400000

infile = open('../data/u_tr_rand_70.csv','rb')
outfile = open('../data/u_tr_rand.csv','wb')

idx = 0
while(idx <= max_tr_num):
    line = infile.readline()
    outfile.write(line)
    idx += 1

infile.close()
outfile.close()

print idx
'''
import csv

infile = open('../data/pred129.csv','rb')
outfile = open('../data/test_set.csv','wb')

u_i_dict = {}
count = 0
idx = 0
for line in infile.readlines():
    its = line.strip().split(',')
    if (its[0],its[1]) not in u_i_dict:
        u_i_dict[(its[0],its[1])] = 1
        outfile.write(line)
        idx += 1 
    count += 1

infile.close()
outfile.close()

print idx,count
'''
