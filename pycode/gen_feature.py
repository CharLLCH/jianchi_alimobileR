#coding: utf-8

'''
feature抽取
'''
import mysql.connector
import sys
sys.path.append('..')
import logging,time

from util.db import mydb
from util.item import item
from util.get_item import get_item,get_raw_conf,get_db_conf
import datetime

import csv
import itertools

cf = get_db_conf()

raw_data = get_raw_conf()

def get_mydb():
    host = cf["host"]
    user = cf["user"]
    passwd = cf["passwd"]
    if passwd == "null":
        passwd = ""

    mdb = mydb(host=host,user=user,passwd=passwd,port=3306)
    return mdb    

max_day = 30

#单线程的先这么写着
mdb = get_mydb()

last_day = datetime.date(2014,12,18)
day129 = datetime.date(2014,12,19)

#将day转化成datetime.date
def turn_day(dt):
    sp = dt.split('-')
    sp = [int(i) for i in sp]
    return datetime.date(sp[0],sp[1],sp[2])

def day_tim_beh():
    day = ["d%s"%(i) for i in range(1,max_day)]
    #for i in [3,7,15]:
    #    day.append('in%sd'%(i))
    beh = ["b%s"%(i) for i in range(1,5)]

    result = list(itertools.product(day,beh))
    result = ["%s_%s"%(i,j) for i,j in result]

    return set(result)
    
#抽象类
class abstract_f:
    def set_type(self,date_set):
        self.date_set = date_set

    def get_type(self):
        return self.date_set
        
    #获取类的名字，用来做特征的名字
    def get_name(self):
        return self.__class__.__name__

    #生成候选特征名字，例如beh1_day2这种
    def get_cand(self):
        pass

    #抽取特征，这个也很好理解，get_cand函数就是在这里用的，然后返回的是个字典
    #{feature1:value1,.....}这种
    def extract(self,tran):
        pass

    #讲特征名转成类名+特征的字典
    def transform(self,udict):
        result = {"%s_%s"%(self.get_name(),i):udict[i] for i in udict}
        return result

    def filed_names(self):
        cand = self.get_cand()
        return ["%s_%s"%(self.get_name(),i) for i in cand]


class feature_time_beh(abstract_f):
    def __init__(self):
        pass

    def get_cand(self):
        return day_tim_beh()

    def get_sql(self,tran):
        return "haha"
        
    def extract(self,tran):
        assert isinstance(tran,item)==True

        td = tran.date
        if self.get_type() == "train":
            td = turn_day(td)
        elif self.get_type() == "test":
            td = last_day
        elif self.get_type() == "pred":
            td = day129
        else:
            td = last_day

        sql_str = self.get_sql(tran)
        sql_result = mdb.select_sql(sql_str)

        result = dict.fromkeys(self.get_cand(),0)
        
        #对于每一条数据，第一位是行为，第二位是日期
        for msql in sql_result:
            dt = msql[1]
            timed = (td-dt).days #日期间隔
            beh = msql[0]

            #先获得单天的1234记录
            if timed > max_day:
                pass
            elif timed >= 1:
                #得到特征字符串
                fstr = "d%s_b%s"%(timed,beh)
                if fstr in result:
                    result[fstr] += 1

                #if timed <= 3:
                #    feat_str = 'in3d_beh%s'%(beh)
                #    result[feat_str] += 1
                #if timed <= 7:
                #    feat_str = 'in7d_beh%s'%(beh)
                #    result[feat_str] += 1
                #if timed <= 15:
                #    feat_str = 'in15d_beh%s'%(beh)
                #    result[feat_str] += 1
            else:
                pass

        res = self.transform(result)

        return res

        
        
#用户在过去n天（n可以为0,1,2...35天，取的比较多的原因是怕最后维度不一样）
#内，的beh次数        
class u_i(feature_time_beh):
    def get_sql(self,tran):
        item = tran.item_id
        user = tran.user_id
        return 'select behavior,ubdate from user_train where item=\"%s\" and user=\"%s\"'%(item,user)
        

#用户在过去n天beh过多少次商品
class y_h(feature_time_beh):
    def get_sql(self,tran):
        user = tran.user_id
        return 'select behavior,ubdate from user_train where user=\"%s\"'%(user)

    
#商品n天内被beh过多少次
class s_p(feature_time_beh):
    def get_sql(self,tran):
        item = tran.item_id
        return 'select behavior,ubdate from user_train where item=\"%s\"'%(item)

#商品所在种类n天内被beh过多少次
class c_i(feature_time_beh):
    def get_sql(self,tran):
        category = tran.item_category
        return 'select behavior,ubdate from user_train where icat=\"%s\"'%(category)


normal_list = []
#append_list = [u_i,y_h,s_p]
append_list = [s_p]

#def main(data_set):
def main(data_set,types):
    #ot = one_tran(dt=data_set)
    ot = get_item(dt=data_set)
    count = 0
    if types == "normal":
        if data_set == "train":
            t = open(raw_data["train_dir"],"w")
            c = open(raw_data['train_clk'],'w')
        elif data_set == "test":
            t = open(raw_data["test_dir"],"w")
            c = open(raw_data['test_clk'],'w')
        elif data_set == "pred":
            t = open(raw_data["pred_dir"],"w")
            c = open(raw_data['pred_clk'],'w')
        else:
            print "有问题"
            sys.exit(1)
        #这是这些类的实例化
        normal_ins = [i() for i in normal_list]
        append_ins = [i() for i in append_list]
        for i in normal_ins:
            i.set_type(data_set)
        for i in append_ins:
            i.set_type(data_set)

        #写入文件
        fileds = []
        for norm in normal_ins:
            fileds.extend(norm.filed_names())
        for app in append_ins:
            fileds.extend(app.filed_names())

        #加入自己的dict
        #s_d = ['u_geo','i_cat','week','hour','click']
        #for i in s_d:
        #    fileds.extend(s_d)

        writer = csv.DictWriter(t,fileds)

        first = {i:i for i in fileds}
        
        writer.writerow(first)
        c.write('label\n')
        
        for tran in ot:
            final = {}
            #s_dict = tran.new_feat()
            if tran.behavior_type == '4':
                tmp = '1\n'
            else:
                tmp = '0\n'
            c.write(tmp)

            for i in append_ins:
                #extract获得每类的字典
                res = i.extract(tran)
                final = dict(final,**res) #字典合并

            #final = dict(final,**s_dict)

            writer.writerow(final)

            count += 1
            if count % 1000 == 0:
                print count

        t.close()
        c.close()
    else:
        if data_set == "train":
            t = open(raw_data["vw_train_dir"],"w")
            #c = open(raw_data['train_clk'],'w')
        elif data_set == "test":
            t = open(raw_data["vw_test_dir"],"w")
            #c = open(raw_data['test_clk'],'w')
        elif data_set == "pred":
            t = open(raw_data["vw_pred_dir"],"w")
            #c = open(raw_data['pred_clk'],'w')
        else:
            print "有问题"
            sys.exit(1)

        #这是这些类的实例化
        normal_ins = [i() for i in normal_list]
        append_ins = [i() for i in append_list]
        for i in normal_ins:
            i.set_type(data_set)
        for i in append_ins:
            i.set_type(data_set)

        for tran in ot:
            #if tran.behavior_type == '4':
            #    tmp = '1\n'
            #else:
            #    tmp = '0\n'
            #c.write(tmp)
            self_dict = tran.new_feat()
            str_line = ''
            if tran.behavior_type == '4':
                str_line += '1 '
            else:
                str_line += '-1 '
            str_line += '%s_%s'%(tran.user_id,tran.item_id)
            for i in append_ins:
                res = i.extract(tran)
                str_line += gen_str(res,i.get_name())
            str_line += gen_str(self_dict,'o_f')
            str_line += '\n'
            t.write(str_line)
            count += 1
            if count % 5000 == 0:
                print '--:->',count

    mdb.dump_cache()

def gen_str(fdict,names):
    tmp_str = '|%s '%(names)
    for key in fdict:
        tmp_str += '%s '%(fdict[key])
    return tmp_str

from optparse import OptionParser 
    
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-d", "--data", dest="data",help="选择数据集，训练还是测试")
    parser.add_option("-t", "--type", dest="type",help="选择那种分类格式")

    (options, args) = parser.parse_args()

    if options.data == "train":
        print "训练集"
        if options.type == "normal":
            main("train","normal")
        else:
            main("train","vw")

    elif options.data == "test":
        print "验证集合"
        if options.type == "normal":
            main("test","normal")
        else:
            main("test","vw")
        
    elif options.data == "pred":
        print "提交集合"
        if options.type == "normal":
            main("pred","normal")
        else:
            main("pred","vw")
        
    else :
        print "error,没有符合的数据集"
        sys.exit(1)
