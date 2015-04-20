#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :remove_doubles.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
infile = open('submit.csv','rb')

outfile = open('new_sub.csv','wb')

uidict = {}

for line in infile.readlines():
    strs = line.strip().split(':')
    if strs[0] not in uidict:
        uidict[strs[0]] = float(strs[1])
    else:
        if float(strs[1]) > uidict[strs[0]]:
            uidict[strs[0]] = float(strs[1])

print len(uidict)

for key in uidict:
    str_tmp = key+':'+'%.3f'%(uidict[key])+'\n'
    outfile.write(str_tmp)

infile.close()
outfile.close()
