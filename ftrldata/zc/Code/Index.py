import size
class Index:
    def __init__(self):
        pass
    
    def __init_list__(self):
        self.item_list = []
        self.category_list = []
        for i in range(item_size):
            self.item_list.append({})
        for i in range(category_size):
            self.category_list.append({})
    def __get_behavior__(self, l, attribute, user_id, time):
        if l[int(attribute)].has_key(user_id):
            if l[int(attribute)][user_id].has_key(time):
                return l[int(attribute)][user_id][time]
        return [0,0,0,0]
    def get_behavior(self, attribute, user_id, time):
        if attribute[0] == 'item':
            return self.__get_behavior__(self.item_list, attribute[1], user_id, time)
        else:
            return self.__get_behavior__(self.category_list, attribute[1], user_id, time)
        
    def load(self, path = '../Data/encode/user.csv'):
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