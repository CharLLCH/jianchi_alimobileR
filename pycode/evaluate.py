#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :evaluate.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
from sklearn.metrics import f1_score,precision_score,recall_score

truth = open('../vwdatatest/vw_feat_test.csv','rb')
pred = open('../vwdatatest/pred','rb')

y_true = []
for line in truth.readlines():
    label = int(line.strip().split(' ')[0])
    if label == 1:
        y_true.append(label)
    else:
        y_true.append(0)
truth.close()

y_pred = []
for line in pred.readlines():
    label = line.strip().split(' ')[0]
    if label == '1.000000':
        y_pred.append(1)
    else:
        y_pred.append(0)
pred.close()

print 'predicted ',sum(y_pred),' positive item.'
print 'precision_score : ',precision_score(y_true,y_pred)
print 'recall_score : ',recall_score(y_true,y_pred)
print 'f1_score : ',f1_score(y_true,y_pred)
