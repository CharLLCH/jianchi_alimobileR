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

from util.get_matrix import get_feat_matrix,get_feat_label
from util.get_item import get_raw_conf
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score,precision_score,recall_score
from optparse import OptionParser

raw_data = get_raw_conf()

'''
print "loding data.."
tr_x = pickle.load(open(raw_data['tr_x'],'rb'))
tr_y = pickle.load(open(raw_data['tr_y'],'rb'))
te_x = pickle.load(open(raw_data['te_x'],'rb'))
te_y = pickle.load(open(raw_data['te_y'],'rb'))
print "data loaded."
'''

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
    tmp_file = open(raw_data['tmp_pred'],'wb')
    pickle.dump(y_list,tmp_file,True)

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
    clf = LogisticRegression(penalty='l1',C=0.5)
    #clf = LogisticRegression()
    y_pred = clf.fit(tr_x,tr_y).predict(te_x)
    print 'predicted ',sum(y_pred),' positive item.'
    print 'precision_score : ',precision_score(te_y,y_pred)
    print 'recall_score : ',recall_score(te_y,y_pred)
    print 'f1_score : ',f1_score(te_y,y_pred)
    save_pred(y_pred)

def RF_predictor(tr_x,tr_y,te_x,te_y):
    '''Random Forest'''
    #clf = RandomForestClassifier(n_estimators=200,max_features="auto",max_depth=8,min_samples_split=10,min_samples_leaf=2,n_jobs=2)
    clf = RandomForestClassifier(n_estimators=15,max_depth=8,n_jobs=2)
    print "start to fit the metricx"
    clf.fit(tr_x,tr_y)
    print "start to predict .."
    y_pred = clf.predict(te_x)
    print '************************'
    print 'predict ',sum(y_pred),' positive item.'
    print 'p_score : ',precision_score(te_y,y_pred)
    print 'r_score : ',recall_score(te_y,y_pred)
    print 'f_score : ',f1_score(te_y,y_pred)
    print '************************'
    save_pred(y_pred)


if __name__ == "__main__":
    
    parser = OptionParser()
    parser.add_option('-d','--data',dest='data',help='test or pred.')

    (options,args) = parser.parse_args()
    
    if options.data == 'test':
        print 'start to loading trx'
        #tr_x = get_feat_matrix(raw_data['train_dir'])
        tr_x = get_feat_matrix(raw_data['tr_cat_dir'])
        print 'start to loading try'
        tr_y = get_feat_label(raw_data['train_clk'])
        print 'start to loading tex'
        #te_x = get_feat_matrix(raw_data['test_dir'])
        te_x = get_feat_matrix(raw_data['te_cat_dir'])
        print 'start to loading tey'
        te_y = get_feat_label(raw_data['test_clk'])
    elif options.data == 'pred':
        print 'start to loading trx'
        tr_x = get_feat_matrix(raw_data['train_dir'])
        print 'start to loading try'
        tr_y = get_feat_label(raw_data['train_clk'])
        print 'start to loading tex'
        te_x = get_feat_matrix(raw_data['pred_dir'])
        print 'start to loading tey'
        te_y = get_feat_label(raw_data['pred_clk'])
    else:
        print 'options is wrong.'
        sys.exit(1)

    #NB_predictor(tr_x,tr_y,te_x,te_y)
    #SGD_predictor(tr_x,tr_y,te_x,te_y)
    #LR_predictor(tr_x,tr_y,te_x,te_y)
    RF_predictor(tr_x,tr_y,te_x,te_y)
