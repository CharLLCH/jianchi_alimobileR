#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :geo_trans.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
str_list = ['uid','iid','icat','date','ugeo','igeo','label']

for days in range(1,16):
    for cat in ['cat','item']:
        for beh in range(1,5):
            str_tmp = '%s_d%s_b%s'%(cat,days,beh)
            str_list.append(str_tmp)

for days in range(1,7):
    for cat in ['yh','sp','lb']:
        for beh in range(1,5):
            str_tmp = '%s_d%s_b%s'%(cat,days,beh)
            str_list.append(str_tmp)

title_str = ','.join(str_list) + '\n'

# TODO uid,iid,icat,date,ugeo,igeo,label : feats

def trans_feat(inpath,outpath):
    infile = open(inpath,'rb')
    outfile = open(outpath,'wb')
    count = 0
    outfile.write(title_str)
    for line in infile.readlines():
        count += 1
        tmplist = line.strip().split(':')
        tmp_str = ','.join(tmplist[0].split(',')) + ','
        tmp_str += ','.join(tmplist[1].split(','))
        tmp_str += '\n'
        outfile.write(tmp_str)
        if count % 10000 == 0:
            print count
    infile.close()
    outfile.close()

if __name__ == "__main__":
    trans_feat('geo/train.csv','ftrl_tr.csv')
    trans_feat('geo/valid.csv','ftrl_te.csv')
    trans_feat('geo/test.csv','ftrl_pr.csv')
