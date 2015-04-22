#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :merge_set.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

in1 = '../data/original/user.csv'
in2 = '../data/original/tianchi_mobile_recommend_train_user.csv'

out = '../data/original/user_merge.csv'

inf1 = open(in1,'rb')
inf2 = open(in2,'rb')

outf = open(out,'wb')

index = 0

outf.write(inf1.readline())

for line in inf1.readlines():
    index += 1
    outf.write(line)
    if index % 100000 == 0:
        print index
inf1.close()
inf2.readline()

for line in inf2.readlines():
    index += 1
    if index % 100000 == 0:
        print index
    outf.write(line)
inf2.close()

outf.close()
