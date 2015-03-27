#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :construct_user.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

'''
    根据之前的统计数据，将每个user的操作，转化成相应的user类，便于计算相似度
'''

import sys
sys.path.append('..')

from util.read_conf import config
from util.user import user
from util.sim_func import user_sim
import unittest
import csv
import pickle

raw_data = config('../conf/raw_data.conf')
ui_path = raw_data['usr_pur_path']

# TODO transform timefeature to union form
def date_trans(week,hour):
    if week in ['Saturday','Sunday']:
        feat_w = 'Weekend'
    else:
        feat_w = 'worked'
    num_hour = int(hour)
    if num_hour > 5 and num_hour <= 8:
        feat_hour = 'I'
    elif num_hour > 8 and num_hour <= 11:
        feat_hour = 'II'
    elif num_hour > 11 and num_hour <= 14:
        feat_hour = 'III'
    elif num_hour > 14 and num_hour <= 18:
        feat_hour = 'IV'
    elif num_hour > 18 and num_hour <= 23:
        feat_hour = 'V'
    else:
        feat_hour = 'VI'
    return feat_w,feat_hour

# TODO uid:iid-behavior-week-hour,next;
def transform_format(ui_line):
    i_dict = {}
    t_dict = {'I':0,'II':0,'III':0,'IV':0,'V':0,'VI':0,'Weekend':0,'worked':0}
    for item in ui_line.split(','):
        #get each item info
        feat = item.split('-')
        #get each feat info
        #construct the feat.
        tmp = feat[0] + '-' + feat[1]
        if tmp in i_dict:
            i_dict[tmp] += int(feat[1])
        else:
            i_dict[tmp] = int(feat[1])
        t_w,t_h = date_trans(feat[2],feat[3])
        t_dict[t_w] += 1
        t_dict[t_h] += 1
    return i_dict,t_dict


def construc_user_matrix(ui_path):
    ui_dict = pickle.load(open(ui_path,'rb'))

    us_func = user_sim()

    user_dict = {}
    
    for key in ui_dict:
        tmp = transform_format(ui_dict[key])
        user_dict[key] = user(key,tmp[0],tmp[1]) 

    # TODO 直接算出来了吧
    #sim_dict = {}
    fieldnames = ['user_1','user_2','similarity']
    writer = csv.writer(file(raw_data['u_u_sim_time'],'wb'))
    writer.writerow(fieldnames)
    idx = 0
    print 'start to calculate the sim_matrix.'
    for f_key in user_dict:
        for s_key in user_dict:
            if int(s_key) > int(f_key):
                sim = us_func.sim(user_dict[f_key],user_dict[s_key])
                #sim_dict[s_key+'-'+f_key] = sim
                row = [s_key,f_key,sim]
                writer.writerow(row)
        idx += 1
        #print 'No.',idx,'products has got the sim.'
        if idx % 99 == 0:
            print idx+1,'users.'

    # TODO 直接存上吧，不然后面速度太慢
    #outfile = open(raw_data['u_u_sim_time'],'wb')
    #pickle.dump(sim_dict,outfile,True)
    print 'sim_matrix has saved.'

    
class Test(unittest.TestCase):
    def setUp(self):
        pass

    def testTransform_format(self):
        line = '42211296-3-Tuesday-20,183865148-2-Thursday-21'
        self.assertEqual(transform_format(line),{'42211296-3':3,'183865148-2':2})

    def testTransform_format(self):
        line = '42211296-3-Tuesday-20,183865148-2-Thursday-21'
        self.assertEqual(transform_format(line),{'I':0,'II':0,'III':0,'IV':0,'V':2,'VI':0,'Weekend':0,'worked':2})


if __name__ == "__main__":
    #unittest.main()
    construc_user_matrix(ui_path)
