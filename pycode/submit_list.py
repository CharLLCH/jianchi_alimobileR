#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :submit_list.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
import sys
sys.path.append('..')

import datetime
import logging
import mysql.connector
import pickle
from optparse import OptionParser
from util.get_item import get_raw_conf,get_db_conf
from sklearn.metrics import f1_score,precision_score,recall_score

raw_data = get_raw_conf()
db_conf = get_db_conf()

# 打开数据库
try:
    conn = mysql.connector.connect(host=db_conf['host'],user=db_conf['user'],passwd=db_conf['passwd'])
except Exception as err:
    logging.error(err)
cur = conn.cursor()
cur.execute('use %s'%(db_conf['db_name']))

# 获得类别列表
def get_cat_dict(flags):
    cat_dict = {}
    if flags == 'pred':
        cat_file = open(raw_data['item_train_path'],'rb')
        for cat_line in cat_file.readlines():
            tmp_list = cat_line.strip().split(',')
            if tmp_list[0] not in cat_dict:
                cat_dict[tmp_list[0]] = tmp_list[2]
        cat_file.close()
        print "get the cat_dict ",len(cat_dict)
    else:
        cat_file = open(raw_data['n_te_time'],'rb')
        for cat_line in cat_file.readlines():
            tmp_list = cat_line.strip().split(',')
            if tmp_list[1] not in cat_dict:
                cat_dict[tmp_list[1]] = tmp_list[4]
        cat_file.close()
        print 'get the cat_dict ',len(cat_dict)
    return cat_dict

# 为了比较结果，还是记录一下post后的整个y_pred吧
#new_pfile = open(raw_data['post_pur'],'wb')
new_pred = []

#cat_dict = get_cat_dict('test')

def make_sub(test_path,click_path,sub_path,ftype):
    cat_dict = get_cat_dict(ftype)
    infile_t = open(test_path,'rb')
    infile_c = open(click_path,'rb')
    out_file = open(sub_path,'wb')
    preout_file = open('../result/no_post_click.csv','wb')
    out_file.write('user_id,item_id\n')
    preout_file.write('user_id,item_id\n')
    idx = 0
    for line in infile_c.readlines():
        ui_line = infile_t.readline()
        if line.strip() == '1':
            ui_list = ui_line.strip().split(',')
            tmp = '%s,%s\n'%(ui_list[0],ui_list[1])
            preout_file.write(tmp)
            flags = True
            #TODO 将后处理的接到这，要加就加不加就直接生成了
            #TODO 给定u_id,i_id判断删不删了
            flags = post_handler(ui_list[0],ui_list[1],cat_dict)
            if flags:
                out_file.write(tmp)
                new_pred.append(1)
                idx += 1
                if idx % 1000 == 0:
                    print idx
            else:
                new_pred.append(0)
        elif line.strip() == '0':
            new_pred.append(0)
        else:
            pass
    infile_c.close()
    infile_t.close()
    out_file.close()
    preout_file.close()
    #get the new_pred \ pre_pred \ y_truth
    pre_pred = pickle.load(open(raw_data['tmp_pred'],'rb'))
    #y_truth = pickle.load(open(raw_data['te_y'],'rb'))
    if ftype == 'test':
        yfile = open(raw_data['test_clk'],'rb')
    else:
        yfile = open(raw_data['pred_clk'],'rb')
    yfile.readline()
    y_truth = []
    for line in yfile.readlines():
        y_truth.append(int(line.strip()))
    yfile.close()
    compare_clk(pre_pred,y_truth,'pre')
    compare_clk(new_pred,y_truth,'post')

def post_handler(u_id,i_id,cat_dict):
    target_date = datetime.date(2014,12,19)
    i_cat = cat_dict[i_id]
    sql_uc = 'select behavior,ubdate from user_train where user=\"%s\" and icat=\"%s\"'%(u_id,i_cat)
    cur.execute(sql_uc)
    uc_result = cur.fetchall()
    flags = False
    for uc in uc_result:
        day_dis = (target_date - uc[1]).days
        if day_dis < 3:
            flags = True
            break
            #if uc[0] == 4:
            #    flags = False
            #    break
            #elif uc[0] == 2 or uc[0] == 3:
            #    flags = True
            #else:
            #    pass
            #    flags = True
    return flags

def compare_clk(y_pred,y_truth,flags):
    print '**************************'
    print '**************************'
    if flags == 'pre':
        print 'Pre_predict: ',sum(y_pred),' positive item.'
        print 'Pre_p_score : ',precision_score(y_truth,y_pred)
        print 'Pre_r_score : ',recall_score(y_truth,y_pred)
        print 'Pre_f_score : ',f1_score(y_truth,y_pred)
    else:
        print 'Post_predict: ',sum(y_pred),' positive item.'
        print 'Post_p_score : ',precision_score(y_truth,y_pred)
        print 'Post_r_score : ',recall_score(y_truth,y_pred)
        print 'Post_f_score : ',f1_score(y_truth,y_pred)
    print '**************************'
    print '**************************'

if __name__ == "__main__":
    
    parser = OptionParser()
    parser.add_option('-t','--type',dest='type',help='选择是test还是pred')

    (options, args) = parser.parse_args()

    if options.type == 'test':
        make_sub(raw_data['n_te_time'],raw_data['test_pur'],raw_data['sub_test'],options.type)
    elif options.type == 'pred':
        make_sub(raw_data['test_set'],raw_data['test_pur'],raw_data['sub_test'],options.type)
    else:
        print "options wrong.."
        sys.exit(1)
