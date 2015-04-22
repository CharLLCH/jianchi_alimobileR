from index import *

def all_zeros(s):
    if sum(s) == 0:
        return True
    else:
        return False


class Basic:
    def __init__(self):
        pass
    def load(self,udir):
        self.search_dic = BasicDictionary(udir)
        
    def generate(self, idir, odir, day):
        print 'generate basic features:', idir
        fi = open(idir)
        fo = open(odir, 'w')
        reader = csv.reader(fi)
        writer = csv.writer(fo)

        title = reader.next()
        attribute = {}
        for i in range(len(title)):
            attribute[title[i]] = i


        for i in range(int(day)):
            for j in range(4):
                title.append('user_item_'+str(i+1)+'_behavior'+str(j+1))
            for j in range(4):
                title.append('user_category_'+str(i+1)+'_behavior'+str(j+1))
        writer.writerow(title)

        cnt = 0
        c1 = 0
        c2 = 0
        for line in reader:
            cnt += 1
            if cnt % 100000 == 0:
                print ' ', cnt
            user_id = line[attribute['user_id']]
            item_id = line[attribute['item_id']]
            item_category = line[attribute['item_category']]
            time = line[attribute['time']]
            label = line[attribute['label']]

            for i in range(int(day)):
                time = str(int(time) - 1)
                line.extend(self.__user_item_time_feature__(user_id, item_id, time)) 
                line.extend(self.__user_category_time_feature__(user_id, item_category, time))

            if all_zeros(line[6:]) == False:
                if label == '1':
                    c1 += 1
                elif label == '0':
                    c2 += 1
                writer.writerow(line)
        print ' ',cnt
        print ' pos',c1
        print ' neg',c2
        fi.close()
        fo.close()
    def __user_item_time_feature__(self, user_id, item_id, time):
        bh = self.search_dic.search_user_item_time(user_id, item_id, time)
        #return rate_feature(bh)
        return bh
    def __user_category_time_feature__(self, user_id, item_category, time):
        bh = self.search_dic.search_user_category_time(user_id, item_category, time)
        #return rate_feature(bh)
        return bh

class Extend:
    def __init__(self):
        pass
    def load(self,udir):
        self.search_dic = ExtendDictionary(udir)
        
    def generate(self, idir, odir, day):
        print 'extend features:', idir
        fi = open(idir)
        fo = open(odir, 'w')
        reader = csv.reader(fi)
        writer = csv.writer(fo)
        title = reader.next()

        attribute = {}
        for i in range(len(title)):
            attribute[title[i]] = i

        for i in range(int(day)):
            for j in range(4):
                title.append('user_'+str(i+1)+'_behavior'+str(j+1))
            for j in range(4):
                title.append('item_'+str(i+1)+'_behavior'+str(j+1))
            for j in range(4):
                title.append('category_'+str(i+1)+'_behavior'+str(j+1))
        writer.writerow(title)

        cnt = 0
        for line in reader:
            cnt += 1
            if cnt % 100000 == 0:
                print ' ', cnt
            
            user_id = line[attribute['user_id']]
            item_id = line[attribute['item_id']]
            item_category = line[attribute['item_category']]
            time = line[attribute['time']]
            label = line[attribute['label']]

            for i in range(int(day)):
                time = str(int(time) - 1)
                line.extend(self.__user_time_feature__(user_id, time))
                line.extend(self.__item_time_feature__(item_id, time))
                line.extend(self.__category_time_feature__(item_category, time))

            writer.writerow(line)
        print ' ',cnt
        fi.close()
        fo.close()
    def __user_time_feature__(self, user_id, time):
        bh = self.search_dic.search_user_time(user_id, time)
        return bh
        #return rate_feature(bh)
    def __item_time_feature__(self, item_id, time):
        bh = self.search_dic.search_item_time(item_id, time)
        return bh
        #return rate_feature(bh)
    def __category_time_feature__(self, item_category, time):
        bh = self.search_dic.search_category_time(item_category, time)
        return bh
        #return rate_feature(bh)

def rate_feature(bh):
    if bh[2] != 0:
        bh.append(round(float(bh[3])/bh[2], 2))
    else:
        bh.append(0)
    if bh[1] != 0:
        bh.extend(round(float(bh[3])/bh[1], 2), round(float(bh[2])/bh[1], 2))
    else:
        bh.extend[0,0]
    if bh[0] != 0:
       bh.extend(round(float(bh[3])/bh[0], 2),round(float(bh[2])/bh[0], 2),  round(float(bh[1])/bh[0], 2))
    else:
        bh.extend([0,0,0])
    return bh
