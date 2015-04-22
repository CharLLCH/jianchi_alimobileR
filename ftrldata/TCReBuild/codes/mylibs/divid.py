'''
Splitter : select valid pos
           generate valid
           generate test
           select train
'''

import random
from index import *
import myio

class Splitter:
    def generate_dev_pos(self, dev_time, udir, odir):
        print 'generate dev pos set:'
        d = DicBuilder(udir).get_dic(['user_id', 'item_id', 'time', 'behavior_type'],[])
        
        pos = []
        for k in d.keys():
            values = k.split(',')
            if values[-1] == '4' and values[-2] in dev_time:
                pos.append([values[0],values[1], values[2]])
        print ' pos:', len(pos)
    
        myio.write_file(odir, ['user_id', 'item_id', 'time'], pos)
        print 'generate dev pos succeed!\n'

    def select_train(self, dev_time, udir, odir, feature_days, scale):
        print 'select train'

        dtmp = DicBuilder(udir).get_dic(['user_id', 'item_id', 'item_category','time', 'behavior_type'])
        d = {}
        for key in dtmp.keys():
            user_id, item_id, item_category, time, behavior_type = key.split(',')
            key = user_id + ',' + item_id + ',' + item_category + ',' + time
            if time not in dev_time and int(time) >= feature_days:
            #if time not in dev_time:
                if d.has_key(key):
                    d[key] = d[key] or (behavior_type == '4')
                else:
                    d[key] = behavior_type == '4'

        neg_train = []
        pos_train = []
        for key in d.keys():
            user_id, item_id, item_category, time = key.split(',')
            if d[key]:
                pos_train.append([user_id, item_id, item_category, time, '1', '?'])
            else:
                neg_train.append([user_id, item_id, item_category, time, '0', '?'])
        print ' train neg',len(neg_train)
        print ' train pos',len(pos_train)
        
        random.shuffle(neg_train)
        pos_train.extend(neg_train[:int(len(pos_train)*scale)])
        random.shuffle(pos_train)
        myio.write_file(odir, ['user_id','item_id','item_category','time','label', 'proba'], pos_train)
        print 'select train succeed!\n'

    def generate(self, time, udir, odir, item_days = 30, category_days = 1, item_dir = ''):
        print 'generate :'
        uitc_dic = DicBuilder(udir).get_dic(['user_id','item_id','time', 'item_category', 'behavior_type'],[])

        s1=set()
        s2=set()
        
        item_dic = DicBuilder(item_dir).get_dic(['item_id'],[])
        s1 = self.__generate_by_item__(time, uitc_dic,item_days,item_dic)
        #s2 = self.__generate_by_category__(time,uitc_dic,category_days,{})
        for s in s2:
            s1.add(s)

        sfinal = []
        for s in s1:
            sfinal.append(s.split(','))
        print ' final fenerate size', len(sfinal)
        
        myio.write_file(odir, ['user_id','item_id','item_category','time','label', 'proba'], sfinal)
        print 'generate succeed!!\n'

    def __generate_by_category__(self, time_cur, uitc_dic, day, item_dic={}):
        print ' generate by category'
        all_category_item_dic = {}
        preday_user_category = {}
        
        for k in uitc_dic.keys():
            [user_id, item_id, time, item_category, behavior_type] = k.split(',')
            if int(time) < int(time_cur) and int(time) >= int(time_cur)-int(day):
                if preday_user_category.has_key(user_id):
                    preday_user_category[user_id].add(item_category)
                else:
                    preday_user_category[user_id] = set()
                    preday_user_category[user_id].add(item_category)
                if behavior_type == '4':
                    if all_category_item_dic.has_key(item_category):
                        all_category_item_dic[item_category].add(item_id)
                    else:
                        all_category_item_dic[item_category] = set()
                        all_category_item_dic[item_category].add(item_id)
        s = set()
        for u in preday_user_category:
            for c in preday_user_category[u]:
                if all_category_item_dic.has_key(c):
                    for i in all_category_item_dic[c]:
                        if len(item_dic) != 0:
                            if item_dic.has_key(i):
                                s.add(u+','+i+','+c+','+time_cur+',?,?')
                        else:
                            s.add(u+','+i+','+c+','+time_cur+',?,?')
        print ' generate size',len(s)
        return s
                
                
    def __generate_by_item__(self, time_cur, uitc_dic, day = 30, item_dic = {}):
        print 'generate by item'
        s = set()
        for k in uitc_dic.keys():
            [user_id, item_id, time, item_category, behavior] = k.split(',')
            if int(time) < int(time_cur) and int(time) >= int(time_cur)-int(day):
                if len(item_dic) != 0:
                    if item_dic.has_key(item_id):
                        s.add(user_id+','+item_id+','+item_category+','+time_cur+',?,?')
                else:
                    s.add(user_id+','+item_id+','+item_category+','+time_cur+',?,?')
        print ' generate size',len(s)
        return s
