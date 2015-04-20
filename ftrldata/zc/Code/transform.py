class Rule:
    def __init__(self):
        pass
    def __write_rule__(self, rule_path, l):
        l.sort()
        f = open(rule_path, 'w')
        for k in l:
            f.write(k+'\n')
        f.close()
    def __analyse_title__(self, title):
        dic = {}
        title = title[:-1].split(',')
        for i in range(len(title)):
            dic[title[i]] = i
        return dic
    def generate(self, user_path = './Data/original/user.csv', rule_path = './Others/TransformRules'):
        print 'generate transform rules'
        f = open(user_path)
        attribute_dic = self.__analyse_title__(f.readline())
        dic_user = {}
        dic_item = {}
        dic_category = {}
        dic_time = {}
        cnt = 0
        for line in f:
            cnt += 1
            if cnt % 1000000 == 0:
                print cnt
            line = line.split(',')
            dic_user[line[attribute_dic['user_id']]] = True
            dic_item[line[attribute_dic['item_id']]] = True
            dic_category[line[attribute_dic['item_category']]] = True
            dic_time[line[attribute_dic['time']].split(' ')[0]] = True
        f.close()
        
        self.__write_rule__(rule_path+'/user.rule', dic_user.keys())
        self.__write_rule__(rule_path+'/item.rule', dic_item.keys())
        self.__write_rule__(rule_path+'/category.rule', dic_category.keys())
        self.__write_rule__(rule_path+'/time.rule', dic_time.keys())
        
        print '  user:\t',len(dic_user)
        print '  item:\t',len(dic_item)
        print '  category:\t',len(dic_category)
        print '  time:\t',len(dic_time)
        del dic_user, dic_item, dic_category, dic_time

class Encoder:
    def __init__(self, path = './Others/TransformRules'):
        self.load_rule()

    def __load_rule__(self, rule_path):
        l = []
        f = open(rule_path)
        for i in f:
            l.append(i[:-1])
        f.close()
        return l
    def load_rule(self, rule_path = './Others/TransformRules'):
        print 'load rule'
        self.dic = {}
        self.dic['user_id'] = self.__load_rule__(rule_path+'/user.rule')
        self.dic['item_id'] = self.__load_rule__(rule_path+'/item.rule')
        self.dic['item_category'] = self.__load_rule__(rule_path+'/category.rule')
        self.dic['time'] = self.__load_rule__(rule_path+'/time.rule')
    
    def decode(self, attribute, n):
        if self.dic.has_key(attribute):
            return self.dic[attribute][int(n)]
        else:
            return n
    def encode(self, attribute, id):
        if self.dic.has_key(attribute):
            return self.__encode__(attribute, id, 0, len(self.dic[attribute])-1)
        else:
            return id
    def __encode__(self, attribute, id, s, e):
        if (s > e):
            return '-1'
        m = (s+e)/2
        if self.dic[attribute][m] == id:
            return str(m)
        elif self.dic[attribute][m] < id:
            return self.__encode__(attribute, id, m+1, e)
        else:
            return self.__encode__(attribute, id, s, m-1)
    
    def encode_file(self, path = './Data/original/user_new.csv', new_path = './Data/encode/user.csv'):#
        print 'encode',path
        f = open(path)
        fw = open(new_path, 'w')
        attribute = f.readline()[:-1]
        fw.write(attribute+'\n')
        attribute = attribute.split(',');
        cnt = 0
        for line in f:
            cnt += 1
            if cnt % 1000000 == 0:
                print cnt
            s = ''
            line = line[:-1].split(',')
            for i in range(len(attribute)):
                s = s + self.encode(attribute[i], line[i])+','
            s = s[:-1]+'\n'
            fw.write(s)
        fw.close()
        f.close()
        print 'complete!',new_path

    def decode_file(self, path = 'result.csv', new_path = 'submit.csv'):
        print 'decode',path
        f = open(path)
        fw = open(new_path, 'w')
        attribute = f.readline()[:-1]
        fw.write(attribute+'\n')
        attribute = attribute.split(',')
        for line in f:
            s = ''
            line = line[:-1].split(',')
            for i in range(len(attribute)):
                s = s + self.decode(attribute[i], line[i])+','
            s = s[:-1]+'\n'
            fw.write(s)
        fw.close()
        f.close()
        print 'complete!',new_path
