#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :sub_to_sub.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
import gzip

infile = gzip.open('test_sub.gz','rb')
infile.readline()
outfile = open('submit.csv','wb')

for line in infile.readlines():
    tmplist = line.strip().split(',')
    ids = tmplist[0].split('-')
    tmpstr = ids[0] + ',' + ids[1] + ':' + tmplist[1] + '\n'
    outfile.write(tmpstr)

outfile.close()
