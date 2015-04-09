#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :get_matrix.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
from get_item import get_raw_conf
import numpy as np

def get_feat_matrix(dpath):
    tmp_m = []
    infile = open(dpath,'rb')
    infile.readline()
    for line in infile.readlines():
        tmp_list = [int(i) for i in line.strip().split(',')]
        tmp_m.append(tmp_list)
    return np.matrix(tmp_m)

def get_feat_label(dpath):
    tmp_l = []
    infile = open(dpath,'rb')
    infile.readline()
    for line in infile.readlines():
        tmp_l.append(int(line.strip()))
    return np.array(tmp_l)
