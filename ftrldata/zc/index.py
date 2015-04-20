'''
Index : get behavior
Dic_Builder : get_dic
'''
import size
class Dic_Builder:
    def __init__(self, path):
        self.path = path
    
    def get_dic(self, key = [], value = []):
        if len(key) == 0:
            return {}
        dic = {}
        f = open(self.path)
        title = f.readline()[0:-1].split(',')
        attribute = {}
        print ' build dictionary: ',key,':',value
        for i in range(len(title)):
            attribute[title[i]] = i
        for line in f:
            line = line[:-1].split(',')
            ky = ''
            vl = ''
            for k in key:
                ky = ky + line[attribute[k]] + ','
            ky = ky[:-1]
            for v in value:
                vl = vl + line[attribute[v]] + ','
            vl = vl[:-1]
            dic[ky] = vl
        f.close()
        return dic

class BasicDictionary:
    def __init__(self, path):
        f = open(path)
        title = f.readline()[:-1].split(',')
        self.attribute = {}
        for i in range(len(title)):
            self.attribute[title[i]] = i

        self.__declear_dic__()
        
        print 'load file', path
        cnt = 0
        for line in f:
            cnt += 1
            if cnt % 1000000 == 0:
                print ' ',cnt
            line = line[:-1].split(',')
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
        for i in range(size.item):
            self.dic['item_time_user'].append({})
        self.dic['user_time_category'] = []
        for i in range(size.user):
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

class UserDictionary:
    '''
    dictionary structure:
    item_user_time_dicitonary:[{time:{user:[0,0,0,0],[],,size.user:[item time behavior]},,,,[item behavior]}
    user_time_categry :[{time:{category:[behavior],...,size.category:[user behavior]},...},...,user_behavior]
    category_day:[time:[category time behavior], ]
    '''
    def __init__(self, path):
        f = open(path)
        title = f.readline()[:-1].split(',')
        self.attribute = {}
        for i in range(len(title)):
            self.attribute[title[i]] = i

        self.__declear_dic__()
        
        print 'load file', path
        cnt = 0
        for line in f:
            cnt += 1
            if cnt % 1000000 == 0:
                print ' ',cnt
            line = line[:-1].split(',')
            self.__build_dic__(line)
        print ' ', cnt
        f.close()

    def search_user_time(self, user_id, time):
        return self.__search_three_level_dictionary__('user_time_category', user_id, time, '-1')
    def search_item_time(self, item_id, time):
        return self.__search_three_level_dictionary__('item_time_user', item_id, time, '-1')
    def search_category_time(self, item_category, time):
        item_category = int(item_category)
        if self.dic['category_time'][item_category].has_key(time):
            return self.dic['categroy_time'][item_category][time]
        return [0,0,0,0]
    def search_user_category_time(self, user_id, item_category, time):
        return self.__search_three_level_dictionary__('user_time_category', user_id, time, item_category)
    def search_user_item_time(self, user_id, item_id, time):
        return self.__search_three_level_dictionary__('item_time_user', item_id, time, user_id, '-1')
    def __search_three_level_dictionary__(self, dic_name, index1, time, key3):
        index1 = int(index1)
        if self.dic[dic_name][index1].has_key(time):
            if self.dic[dic_name][index1][time].has_key(key3):
                return self.dic[dic_name][index1][time][key3]
        return [0,0,0,0]
    def __declear_dic__(self):
        self.dic = {}
        self.dic['item_time_user'] = []
        for i in range(size.item):
            self.dic['item_time_user'].append({})
        self.dic['user_time_category'] = []
        for i in range(size.user):
            self.dic['user_time_category'].append({})
        self.dic['category_time'] = []
        for i in range(size.category):
            self.dic['category_time'].append({})
        
    def __build_dic__(self, line):
        user_id = line[self.attribute['user_id']]
        item_id = line[self.attribute['item_id']]
        behavior_type = int(line[self.attribute['behavior_type']])-1
        item_category = line[self.attribute['item_category']]
        time = line[self.attribute['time']]
        self.__category_time__(item_category, time, behavior_type)
        self.__three_level_dictionary__('item_time_user', item_id, time, user_id, behavior_type)
        self.__three_level_dictionary__('user_time_category', user_id, time, item_category, behavior_type)
        
    def __category_time__(self, item_category, time, behavior_type):
        item_category = int(item_category)
        #category_tiem
        if self.dic['category_time'][item_category].has_key(time):
            self.dic['category_time'][item_category][time][behavior_type] += 1
        else:
            self.dic['category_time'][item_category][time] = [0,0,0,0]
            self.dic['category_time'][item_category][time][behavior_type] += 1
        #cateogry
        if self.dic['category_time'][item_category].has_key('-1'):
            self.dic['category_time'][item_category]['-1'][behavior_type] += 1
        else:
            self.dic['category_time'][item_category]['-1'] = [0,0,0,0]
            self.dic['category_time'][item_category]['-1'][behavior_type] += 1
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
        #index1 time
        if self.dic[dic_name][index1][time2].has_key('-1'):
            self.dic[dic_name][index1][time2]['-1'][behavior_type] += 1
        else:
            self.dic[dic_name][index1][time2]['-1'] = [0,0,0,0]
            self.dic[dic_name][index1][time2]['-1'][behavior_type] = 1
        #index1 
        if self.dic[dic_name][index1].has_key('-1'):
            self.dic[dic_name][index1]['-1'][behavior_type] += 1
        else:
            self.dic[dic_name][index1]['-1'] = [0,0,0,0]
            self.dic[dic_name][index1]['-1'][behavior_type] = 1
class ExtendDictionary:
    def __init__(self, path):
        f = open(path)
        title = f.readline()[:-1].split(',')
        self.attribute = {}
        for i in range(len(title)):
            self.attribute[title[i]] = i

        self.__declear_dic__()
        
        print 'load file', path
        cnt = 0
        for line in f:
            cnt += 1
            if cnt % 1000000 == 0:
                print ' ',cnt
            line = line[:-1].split(',')
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
        for i in range(size.item):
            self.dic['item_time'].append({})
        self.dic['user_time'] = []
        for i in range(size.user):
            self.dic['user_time'].append({})
        self.dic['category_time'] = []
        for i in range(size.category):
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
            
class UserDayIndex:
    def __init__(self):
        pass
    
    def load(self, user):
        f = open(user)
        
        title = f.readline()[:-1].split(',')
        attribute = {}
        for i in range(len(title)):
            attribute[title[i]] = i
            
        self.dic = []
        for i in range(size.user):
            self.dic.append({})
        
        cnt = 0
        for line in f:
            cnt += 1
            if cnt % 1000000 == 0:
                print ' ', cnt
            line = line[:-1].split(',')
            uid = int(line[attribute['user_id']])
            time = line[attribute['time']]
            behavior = int(line[attribute['behavior_type']]) - 1
            if self.dic[uid].has_key(time):
                self.dic[uid][time][behavior] += 1
            else:
                self.dic[uid][time] = [0,0,0,0]
                self.dic[uid][time][behavior] = 1
        f.close()
        self.normalization()
    def normalization(self):
        for i in range(size.user):
            for key in self.dic[i].keys():
                s = sum(self.dic[i][key])
                if self.dic[i][key][0] == 0:
                    self.dic[i][key][0] = 0.0
                else:
                    self.dic[i][key][0] = 10.0*self.dic[i][key][0]/s
                if self.dic[i][key][1] == 0:
                    self.dic[i][key][1] = 0.0
                else:
                    self.dic[i][key][1] = 10.0*self.dic[i][key][1]/s
                if self.dic[i][key][2] == 0:
                    self.dic[i][key][2] = 0.0
                else:
                    self.dic[i][key][2] = 10.0*self.dic[i][key][2]/s
                if self.dic[i][key][3] == 0:
                    self.dic[i][key][3] = 0.0
                else:
                    self.dic[i][key][3] = 10.0*self.dic[i][key][3]/s
                
    def release(self):
        del self.dic
    def search(self, user, day):
        if self.dic[user].has_key(day):
            return self.dic[user][day]
        else:
            return [0,0,0,0]
class Index:
    def __init__(self):
        pass
    
    def __init_list__(self):
        self.item_list = []
        self.category_list = []
        for i in range(size.item):
            self.item_list.append({})
        for i in range(size.category):
            self.category_list.append({})
    def __get_behavior__(self, l, attribute, user_id, time):
        if l[int(attribute)].has_key(user_id):
            if l[int(attribute)][user_id].has_key(time):
                return l[int(attribute)][user_id][time]
        return [0,0,0,0]
    def get_behavior(self, attribute, id, time):
        if attribute[0] == 'item':
            return self.__get_behavior__(self.item_list, attribute[1], id, time)
        else:
            return self.__get_behavior__(self.category_list, attribute[1], id, time)
        
    def load(self, path = './Data/encode/user.csv'):
        print 'load'
        self.__init_list__()
        f = open(path)
        
        title = f.readline()[:-1].split(',')
        attribute = {}
        for i in range(len(title)):
            attribute[title[i]] = i
        
        cnt = 0
        for line in f:
            cnt += 1
            if cnt % 1000000 == 0:
                print ' ',cnt
            line = line[:-1].split(',')

            user_id = line[attribute['user_id']]
            item_id = line[attribute['item_id']]
            behavior_type = int(line[attribute['behavior_type']])-1
            item_category = line[attribute['item_category']]
            time = line[attribute['time']]
        
            if self.item_list[int(item_id)].has_key(user_id):
                if self.item_list[int(item_id)][user_id].has_key(time):
                    self.item_list[int(item_id)][user_id][time][behavior_type] += 1
                else:
                    self.item_list[int(item_id)][user_id][time] = [0,0,0,0]
                    self.item_list[int(item_id)][user_id][time][behavior_type] = 1
            else:
                self.item_list[int(item_id)][user_id] = {}
                self.item_list[int(item_id)][user_id][time] = [0,0,0,0]
                self.item_list[int(item_id)][user_id][time][behavior_type] = 1
        
            if self.category_list[int(item_category)].has_key(user_id):
                if self.category_list[int(item_category)][user_id].has_key(time):
                    self.category_list[int(item_category)][user_id][time][behavior_type] += 1
                else:
                    self.category_list[int(item_category)][user_id][time] = [0,0,0,0]
                    self.category_list[int(item_category)][user_id][time][behavior_type] = 1
            else:
                self.category_list[int(item_category)][user_id] = {}
                self.category_list[int(item_category)][user_id][time] = [0,0,0,0]
                self.category_list[int(item_category)][user_id][time][behavior_type] = 1
