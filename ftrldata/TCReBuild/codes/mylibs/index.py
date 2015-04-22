'''
Index : get behavior
Dic_Builder : get_dic
'''
import size
import csv
class DicBuilder:
    def __init__(self, path):
        self.path = path
    
    def get_dic(self, key = [], value = []):
        if len(key) == 0 or len(self.path) == 0:
            return {}
        dic = {}
        
        f = open(self.path)
        reader = csv.reader(f)
        title = reader.next()
        
        att = {}
        print ' build dictionary: ',key,':',value
        for i in range(len(title)):
            att[title[i]] = i

        for line in reader:

            ky = ''
            vl = ''
            for k in key:
                ky = ky + line[att[k]] + ','
            ky = ky[:-1]
            for v in value:
                vl = vl + line[att[v]] + ','
            vl = vl[:-1]
            dic[ky] = vl
        f.close()
        return dic

class BasicDictionary:
    def __init__(self, path):
        f = open(path)
        reader = csv.reader(f)
        title = reader.next()
        self.attribute = {}
        for i in range(len(title)):
            self.attribute[title[i]] = i

        self.__declear_dic__()
        
        print 'load file', path
        cnt = 0
        for line in reader:
            cnt += 1
            if cnt % 1000000 == 0:
                print ' ',cnt
            self.__build_dic__(line)
        print ' ', cnt
        f.close()

    def search_user_category_time(self, user_id, item_category, time):
        return self.__search_three_level_dictionary__('user_time_category', user_id, time, item_category)
    def search_user_item_time(self, user_id, item_id, time):
        return self.__search_three_level_dictionary__('item_time_user', item_id, time, user_id)
    def __search_three_level_dictionary__(self, dic_name, index1, time, key3):
        index1 = int(index1)
        if self.dic[dic_name][index1].has_key(time):
            if self.dic[dic_name][index1][time].has_key(key3):
                return self.dic[dic_name][index1][time][key3]
        return [0,0,0,0]
    def __declear_dic__(self):
        self.dic = {}
        self.dic['item_time_user'] = []
        for i in range(size.item_id):
            self.dic['item_time_user'].append({})
        self.dic['user_time_category'] = []
        for i in range(size.user_id):
            self.dic['user_time_category'].append({})
        
    def __build_dic__(self, line):
        user_id = line[self.attribute['user_id']]
        item_id = line[self.attribute['item_id']]
        behavior_type = int(line[self.attribute['behavior_type']])-1
        item_category = line[self.attribute['item_category']]
        time = line[self.attribute['time']]
        self.__three_level_dictionary__('item_time_user', item_id, time, user_id, behavior_type)
        self.__three_level_dictionary__('user_time_category', user_id, time, item_category, behavior_type)
        
    def __three_level_dictionary__(self, dic_name, index1, time2, key3, behavior_type):
        index1 = int(index1)
        #index1 time2, key3
        if self.dic[dic_name][index1].has_key(time2):
            if self.dic[dic_name][index1][time2].has_key(key3):
                self.dic[dic_name][index1][time2][key3][behavior_type] += 1
            else:
                self.dic[dic_name][index1][time2][key3] = [0,0,0,0]
                self.dic[dic_name][index1][time2][key3][behavior_type] = 1
        else:
            self.dic[dic_name][index1][time2] = {}
            self.dic[dic_name][index1][time2][key3] = [0,0,0,0]
            self.dic[dic_name][index1][time2][key3][behavior_type] = 1

class ExtendDictionary:
    def __init__(self, path):
        f = open(path)
        reader = csv.reader(f)
        title = reader.next()
        self.attribute = {}
        for i in range(len(title)):
            self.attribute[title[i]] = i

        self.__declear_dic__()
        
        print 'load file', path
        cnt = 0
        for line in reader:
            cnt += 1
            if cnt % 1000000 == 0:
                print ' ',cnt
            self.__build_dic__(line)
        print ' ', cnt
        f.close()

    def search_user_time(self, user_id, time):
        return self.__search_two_level_dictionary__('user_time', user_id, time)
    def search_item_time(self, item_id, time):
        return self.__search_two_level_dictionary__('item_time', item_id, time)
    def search_category_time(self, item_category, time):
        return self.__search_two_level_dictionary__('category_time', item_category, time)
    def __search_two_level_dictionary__(self, dic_name, index1, time2):
        index1 = int(index1)
        if self.dic[dic_name][index1].has_key(time2):
            return self.dic[dic_name][index1][time2]
        return [0,0,0,0]
    def __declear_dic__(self):
        self.dic = {}
        self.dic['item_time'] = []
        for i in range(size.item_id):
            self.dic['item_time'].append({})
        self.dic['user_time'] = []
        for i in range(size.user_id):
            self.dic['user_time'].append({})
        self.dic['category_time'] = []
        for i in range(size.item_category):
            self.dic['category_time'].append({})
        
    def __build_dic__(self, line):
        user_id = line[self.attribute['user_id']]
        item_id = line[self.attribute['item_id']]
        behavior_type = int(line[self.attribute['behavior_type']])-1
        item_category = line[self.attribute['item_category']]
        time = line[self.attribute['time']]
        self.__two_level_dictionary__('category_time', item_category, time, behavior_type)
        self.__two_level_dictionary__('item_time', item_id, time, behavior_type)
        self.__two_level_dictionary__('user_time', user_id, time, behavior_type)
        
    def __two_level_dictionary__(self, dic_name, index1, time2, behavior_type):
        index1 = int(index1)
        if self.dic[dic_name][index1].has_key(time2):
            self.dic[dic_name][index1][time2][behavior_type] += 1
        else:
            self.dic[dic_name][index1][time2] = [0,0,0,0]
            self.dic[dic_name][index1][time2][behavior_type] = 1
