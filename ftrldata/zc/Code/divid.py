import size
import random
from Index import Dic_Builder
class Splitter:
    def generate_valid_pos(self, valid_day = '30', user_path = './Data/encode/user.csv', output_path = './Data/divid/valid_pos.csv'):
        print 'generate valid pos set'
        ur = Dic_Builder(user_path)
        d = ur.get_dic(['user_id','item_id','time','behavior_type'],[])
        pos = []
        for k in d.keys():
            values = k.split(',')
            if values[-1] == '4' and values[-2] == valid_day:
                pos.append(values[0]+','+values[1])
        print ' pos:', len(pos)
        
        f = open(output_path, 'w')
        f.write('user_id,item_id\n')
        for i in pos:
            f.write(i+'\n')
        f.close()
    def generate_valid(self, time = '30', user_path = './Data/encode/user.csv', output_path = './Data/divid/valid.csv', day = 30):
        self.__generate_by_item__(time,user_path,output_path,day)

    def generate_test(self, time = '31', user_path = './Data/encode/user.csv', item_path = '', output_path = './Data/divid/valid.csv', day = 30):
        ur = Dic_Builder(item_path)
        item_dic = ur.get_dic(['item_id'],['item_category'])
        self.__generate_by_item__(time, user_path,output_path,day,item_dic)
        
        
    def __generate_by_item__(self, time = '30', user_path = './Data/encode/user.csv', output_path = './Data/divid/valid.csv', day = 30, item_id = {}):
        ur = Dic_Builder(user_path)
        d = ur.get_dic(['user_id','item_id','time'],['item_category'])
        
        s = set()
        for k in d.keys():
            keys = k.split(',')
            if int(keys[-1]) < int(time) and int(keys[-1]) >= int(time)-int(day):
                if len(item_id) != 0:
                    if item_id.has_key(keys[1]):
                        s.add(keys[0]+','+keys[1]+','+d[k]+','+time+',?')
                else:
                    s.add(keys[0]+','+keys[1]+','+d[k]+','+time+',?')
        print ' generate size',len(s)
        l = []
        l.extend(s)
        self.__write_data__(output_path, [], l, len(s))
    
    def select_train(self, valid_time = '30', user_path = './Data/encode/user.csv', train_path = './Data/divid/train.csv', neg_scale = 5):
        print 'select train'
        d = self.__load_data__(user_path)
        neg_train = []
        pos_train = []
        for key in d.keys():
            if d[key]:
                if key.split(',')[-1] != valid_time:
                    pos_train.append(key + ',1')
            else:
                if key.split(',')[-1] != valid_time:
                    neg_train.append(key + ',0')
        print ' train neg',len(neg_train)
        print ' train pos',len(pos_train)
        self.__write_data__(train_path, pos_train, neg_train, neg_scale*len(pos_train))
        print 'Complete!'

    def __write_data__(self, path, pos, neg, neg_size):
        print 'write_date',path
        random.shuffle(neg)
        pos.extend(neg[0:neg_size])
        random.shuffle(pos)

        f = open(path, 'w')
        f.write('user_id,item_id,item_category,time,label\n')
        for p in pos:
            f.write(p+'\n')
        f.close()
    def __load_data__(self, path):
        print 'load_data',path
        f = open(path)

        attribute = {}
        title = f.readline()[:-1].split(',')
        for i in range(len(title)):
            attribute[title[i]] = i
        
        dic = {}
        cnt = 0
        for line in f:
            cnt += 1
            if cnt % 1000000 == 0:
                print ' ',cnt
            line = line[:-1].split(',')
            key = line[attribute['user_id']] + ',' + line[attribute['item_id']] + ',' + line[attribute['item_category']] + ',' + line[attribute['time']];
            if dic.has_key(key):
                dic[key] = dic[key] or (line[attribute['behavior_type']] == '4')
            else:
                dic[key] = (line[attribute['behavior_type']] == '4')
        
        f.close()
        
        return dic
