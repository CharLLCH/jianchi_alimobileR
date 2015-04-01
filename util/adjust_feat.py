#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :adjust_feat.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

from get_item import get_raw_conf
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score

raw_data = get_raw_conf()

tr_path = raw_data['f_tr_rand']
cr_path = raw_data['f_tr_rand_click']
te_path = raw_data['f_te_rand']
ce_path = raw_data['f_te_rand_click']

max_num = 500000

def get_train_matrix(x_path,flag):
    infile = open(x_path,'rb')
    tr_matrix = []
    if flag == "train":
        idx = 0
        while(idx <= max_num):
            line = infile.readline()
            tmp_list = [int(i) for i in line.strip().split(',')]
            tr_matrix.append(tmp_list)
            idx += 1
    else:
        for line in infile.readlines():
            tmp_list = [int(i) for i in line.strip().split(',')]
            tr_matrix.append(tmp_list)

    return tr_matrix

def get_click_vector(y_path,flag):
    infile = open(y_path,'rb')
    cl_vec = []
    if flag == 'train':
        idx = 0
        while(idx <= max_num):
            line = infile.readline()
            cl_vec.append(int(line.strip()))
            idx +=  1
    else:
        for line in infile.readlines():
            cl_vec.append(int(line.strip()))

    return cl_vec

def check_it(y_pred,y_true):
    num = len(y_pred)
    count = 0
    for i in range(num):
        if y_pred[i] == y_true[i]:
            count += 1

    print num,count


if __name__ == "__main__":
    print "start to load the data..."
    tr_x = get_train_matrix(tr_path,'test')
    print len(tr_x)
    tr_y = get_click_vector(cr_path,'test')
    te_x = get_train_matrix(te_path,'test')
    print len(te_x)
    te_y = get_click_vector(ce_path,'test')
    print "data loaded..."

    gnb = GaussianNB()
    
    y_pred = gnb.fit(tr_x,tr_y).predict(te_x)

    check_it(y_pred,te_y)
    
    print sum(te_y),sum(y_pred)
    
    print f1_score(te_y,y_pred)
