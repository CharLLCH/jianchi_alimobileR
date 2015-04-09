#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :ftrl_feat.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
import sys
sys.path.append('..')

def gen_feat(dir_path,feat_path,ft_path):
    dir_file = open(dir_path,'rb')
    feat_file = open(feat_path,'rb')
    ft_file = open(ft_path,'wb')

    f1 = dir_file.readline().strip().split(',')
    f2 = feat_file.readline()
    tmp_fileds = ','.join(f1[:-1]) + ','
    tmp_fileds += f2
    ft_file.write(tmp_fileds)

    for line in dir_file.readlines():
        x = ','.join(line.strip().split(',')[:-1]) + ','
        x += feat_file.readline()
        ft_file.write(x)

    dir_file.close()
    feat_file.close()
    ft_file.close()


if __name__ == "__main__":
    #gen_feat('../data/n_tr_time.csv','../data/feat_train.csv','../data/ftrl_tr.csv')
    #gen_feat('../data/n_te_time.csv','../data/feat_test.csv','../data/ftrl_te.csv')
    gen_feat('../data/test_set.csv','../data/feat_pred.csv','../data/ftrl_pr.csv')
