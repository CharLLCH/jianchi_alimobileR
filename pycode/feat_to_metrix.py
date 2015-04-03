#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :feat_to_metrix.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
import sys
sys.path.append('..')

from util.get_item import get_raw_conf
import pickle

raw_data = get_raw_conf()

tr_path = raw_data['f_tr_rand']
cr_path = raw_data['f_tr_rand_click']
te_path = raw_data['f_te_rand']
ce_path = raw_data['f_te_rand_click']

def get_train_matrix(x_path):
    infile = open(x_path,'rb')
    tr_metrix = []
    for line in infile.readlines():
        tmp_list = [int(i) for i in line.strip().split(',')]
        tr_metrix.append(tmp_list)
    return tr_metrix

def get_click_vector(y_path):
    infile = open(y_path,'rb')
    cl_vec = []
    for line in infile.readlines():
        cl_vec.append(int(line.strip()))
    return cl_vec

if __name__ == "__main__":
    print "start to dump the data..."
    tr_x = get_train_matrix(tr_path)
    tr_y = get_click_vector(cr_path)
    te_x = get_train_matrix(te_path)
    te_y = get_click_vector(ce_path)

    infile = open(raw_data['tr_x'],'wb')
    pickle.dump(tr_x,infile,True)
    infile.close()
    print 'tr_x dumped...'

    infile = open(raw_data['tr_y'],'wb')
    pickle.dump(tr_y,infile,True)
    infile.close()
    print 'tr_y dumped...'

    infile = open(raw_data['te_x'],'wb')
    pickle.dump(te_x,infile,True)
    infile.close()
    print 'te_x dumped...'

    infile = open(raw_data['te_y'],'wb')
    pickle.dump(te_y,infile,True)
    infile.close()

    print "metrix dumped!.."
