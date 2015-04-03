#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :adjust_feat.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
import sys
sys.path.append('..')

import pickle

from util.get_item import get_raw_conf
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score,precision_score,recall_score

raw_data = get_raw_conf()

print "loding data.."
tr_x = pickle.load(open(raw_data['tr_x'],'rb'))
tr_y = pickle.load(open(raw_data['tr_y'],'rb'))
te_x = pickle.load(open(raw_data['te_x'],'rb'))
te_y = pickle.load(open(raw_data['te_y'],'rb'))
print "data loaded."

def check_it(y_pred,y_true):
    ''' 有待加强，可以输出一些比较关心的信息'''
    num = len(y_pred)
    count = 0
    for i in range(num):
        if y_pred[i] == y_true[i]:
            count += 1
    print num,count

def save_pred(y_list):
    outfile = open(raw_data['test_pur'],'wb')
    outfile.write('click\n')
    for i in y_list:
        tmp = '%s\n'%(i)
        outfile.write(tmp)
    outfile.close()

def NB_predictor(tr_x,tr_y,te_x,te_y):
    ''' Naive Bayes predictor '''
    print 'NB starting...'
    gnb = GaussianNB()
    y_pred = gnb.fit(tr_x,tr_y).predict(te_x)
    print 'predicted ',sum(y_pred),' positive item.'
    print 'precision_score : ',precision_score(te_y,y_pred)
    print 'recall_score : ',recall_score(te_y,y_pred)
    print 'f1_score : ',f1_score(te_y,y_pred)
    save_pred(y_pred)


def SGD_predictor(tr_x,tr_y,te_x,te_y):
    ''' Stochastic Gradient Descent'''
    print 'SGD starting...'
    clf = SGDClassifier(penalty='l2')
    y_pred = clf.fit(tr_x,tr_y).predict(te_x)
    print 'predicted ',sum(y_pred),' positive item.'
    print 'precision_score : ',precision_score(te_y,y_pred)
    print 'recall_score : ',recall_score(te_y,y_pred)
    print 'f1_score : ',f1_score(te_y,y_pred)
    save_pred(y_pred)

def LR_predictor(tr_x,tr_y,te_x,te_y):
    ''' LogisticRegression '''
    print 'LR starting...'
    clf = LogisticRegression(penalty='l2',C=0.05)
    #clf = LogisticRegression()
    y_pred = clf.fit(tr_x,tr_y).predict(te_x)
    print 'predicted ',sum(y_pred),' positive item.'
    print 'precision_score : ',precision_score(te_y,y_pred)
    print 'recall_score : ',recall_score(te_y,y_pred)
    print 'f1_score : ',f1_score(te_y,y_pred)
    save_pred(y_pred)

def RF_predictor():
    '''Random Forest'''
    clf = RandomForestClassifier(n_estimators=1000,max_features="auto",max_depth=8,min_samples_split=10,min_samples_leaf=2)
    print "start to fit the metricx"
    clf.fit(tr_x,tr_y)
    print "start to predict .."
    y_pred = clf.predict(te_x)
    print 'predicted ',sum(y_pred),' positive item.'
    print 'precision_score : ',precision_score(te_y,y_pred)
    print 'recall_score : ',recall_score(te_y,y_pred)
    print 'f1_score : ',f1_score(te_y,y_pred)
    save_pred(y_pred)

    



if __name__ == "__main__":

    #NB_predictor(tr_x,tr_y,te_x,te_y)
    #SGD_predictor(tr_x,tr_y,te_x,te_y)
    #LR_predictor(tr_x,tr_y,te_x,te_y)
