import size
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
    def get_behavior(self, attribute, user_id, time):
        if attribute[0] == 'item':
            return self.__get_behavior__(self.item_list, attribute[1], user_id, time)
        else:
            return self.__get_behavior__(self.category_list, attribute[1], user_id, time)
        
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

class Global:
    def __init__(self):
        pass

    def generate(self,path = './Data/encode/user.csv', new_path = './Features/global/'):
        print 'global features'
        f = open(path)
        title = f.readline()[:-1].split(',')
        attribute = {}
        for i in range(len(title)):
            attribute[title[i]] = i
        
        user = []
        item = []
        category = []
        for i in range(user_size):
            user.append([0,0,0,0])
        for i in range(item_size):
            item.append([0,0,0,0])
        for i in range(category_size):
            category.append([0,0,0,0])
        
        cnt = 0
        for line in f:
            cnt += 1
            if cnt % 1000000 == 0:
                print ' ',cnt
            line = line[:-1].split(',')
            behavior = int(line[attribute['behavior_type']])-1
            user[int(line[attribute['user_id']])][behavior] += 1
            item[int(line[attribute['item_id']])][behavior] += 1
            category[int(line[attribute['item_category']])][behavior] += 1
        f.close()
        
        self.__write_global_features__(new_path+'user.csv', user)
        self.__write_global_features__(new_path+'item.csv', item)
        self.__write_global_features__(new_path+'category.csv', category)
    def __write_global_features__(self, path, l):
        print 'write',path
        f = open(path, 'w')
        for i in l:
            f.write(str(i[0])+','+str(i[1])+','+str(i[2])+','+str(i[3])+'\n')
        f.close()
class DaysFeature():
    def generate(self, obj, output):
        print 'generate:',obj
        l = 0
        if obj == 'item_id':
            l = size.item
        elif obj == 'user_id':
            l = size.user
        else:
            l = size.category
        
        arr = []
        for i in range(l):
            arr.append([])
            for j in range(size.day):
                arr[i].extend([0,0,0,0])

        for line in self.user_file:
            id = int(line[self.attribute[obj]])
            time = int(line[self.attribute['time']])
            behavior = int(line[self.attribute['behavior_type']])-1
            arr[id][4*time+behavior] += 1
        self.__write__(arr,output)

    def load_user(self, user_path):
        print 'load_user'
        self.user_file = []
        
        f = open(user_path)
        title = f.readline()[:-1].split(',')
        self.attribute = {}
        
        for i in range(len(title)):
            self.attribute[title[i]] = i
        for line in f:
            self.user_file.append(line[:-1].split(','))
        f.close()
        
    def __write__(self, arr, output):
        f = open(output, 'w')
        for i in arr:
            s = ''
            for j in i:
                s = s + str(j)+','
            f.write(s[:-1]+'\n')
        f.close()

class Cross:
    def __init__(self):
        pass
    def load(self, path = './Data/encode/user.csv'):
        self.index = Index()
        self.index.load(path)
    def release(self):
        del self.index
    def cross_features(self, input_path = './Data/divid/train.csv', output1 = './Features/train/train.csv', output2 = './Features/train/train_del.csv', day = 7):
        print 'cross feature', input_path

        f = open(input_path)
        f1 = open(output1, 'w')
        f2 = open(output2, 'w')

        title = f.readline()[:-1].split(',')
        attribute = {}
        for i in range(len(title)):
            attribute[title[i]] = i

        cnt = 0
        c1 = 0
        c2 = 0
        for line in f:
            cnt += 1
            if cnt % 100000 == 0:
                print ' ', cnt
            
            #s = line[:-1]+':'
            line = line[:-1].split(',')
            
            user_id = line[attribute['user_id']]
            item_id = line[attribute['item_id']]
            item_category = line[attribute['item_category']]
            s = user_id+','+item_id+','+item_category+','+line[attribute['time']]+','+line[attribute['label']]+':'
                #print line[attribute['time']],
            for i in range(int(day)):
                time = str(int(line[attribute['time']])-1-i)
                #print time,
                behavior = self.index.get_behavior(['category', item_category], user_id, time)
                s = s + str(behavior[0])+','+str(behavior[1])+','+str(behavior[2])+','+str(behavior[3])+','
                behavior = self.index.get_behavior(['item', item_id], user_id, time)
                s = s + str(behavior[0])+','+str(behavior[1])+','+str(behavior[2])+','+str(behavior[3])+','
            
            if self.__all_zeros__(s[:-1].split(':')[1]):
                #f2.write(s[:-1]+'\n')
                if line[attribute['label']] == '1':
                    c1 += 1
                else:
                    c2 += 1
            else:
                f1.write(s[:-1]+'\n')
                #print ''
        f.close()
        f1.close()

        f2.write(str(c1)+'\n'+str(c2)+'\n')
        f2.close()
    def __all_zeros__(self, s):
        for i in s.split(','):
            if i != '0':
                return False
        return True

class Combine:
    def __init__(self):
        pass
    def combine_feature(self, input_path = './Features/train/train.csv', output_path = './Features/train/train_final.csv'):
        print 'combin',input_path
        f = open(input_path)
        fw = open(output_path, 'w')
        for line in f:
            [id, feature] = line[0:-1].split(':')
            [user_id, item_id, item_category, day, label] = id.split(',')
            fw.write(id+':'+feature+','+self.user[int(user_id)]+','+self.item[int(item_id)]+','+self.category[int(item_category)]+'\n')
        f.close()
        fw.close()
    def load_global_feature(self, path = './Features/global/'):
        print 'load global feature'
        self.category = self.__load_global_feature(path+'category.csv')
        self.item = self.__load_global_feature(path+'item.csv')
        self.user = self.__load_global_feature(path+'user.csv')
    def __load_global_feature(self, path):
        f = open(path)
        c = f.read().split('\n')
        return c[0:-1]
