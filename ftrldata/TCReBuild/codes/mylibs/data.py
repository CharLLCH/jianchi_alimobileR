import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from index import Dic_Builder
class data_opt:
    def __init__(self):
        pass
    def load(self,path = '../Features/train/train_final.csv'):
        print 'load', path
        f = open(path)
        ids = []
        X = []
        y = []
        cnt = 0
        for line in f:
            cnt += 1
            if cnt % 100000 == 0:
                print ' ',cnt
            x = []
            [id, feature] = line[0:-1].split(':')
            [user_id, item_id, item_category, day, label] = id.split(',')
            for i in feature.split(','):
                x.append(float(i))
            X.append(x)
            if label != '?':
                y.append(int(label))
            #ids.append(user_id+','+item_id+'\n')
        f.close()
        print ' ',cnt
        return np.array(X,dtype=float), np.array(y,dtype=int), ids
    
    def quick_sort(self, s, e, ids, y):
        if s >= e:
            return
        selected = [ids[s], y[s]]
        m = s
        p = m + 1
        while p <= e:
            if y[p] < selected[1]:
                y[m] = y[p]
                ids[m] = ids[p]
                m += 1
                y[p] = y[m]
                ids[p] = ids[m]
            p += 1
        ids[m] = selected[0]
        y[m] = selected[1]
        self.quick_sort(s, m-1, ids, y)
        self.quick_sort(m+1, e, ids, y)
    def write(self, path, ids, y):
        #self.quick_sort(0, len(y)-1, ids, y)
        f = open(path, 'w')
        f.write('user_id,item_id,proba\n')
        for i in range(len(y)):
            f.write(ids[i]+':'+str(y[i])+'\n')
        f.close()
    def read(self, path):
        f = open(path)
        f.readline()
        ids = []
        y = []
        for line in f:
            line = line[0:-1].split(':')
            ids.append(line[0])
            y.append(float(line[1]))
        f.close()
        return ids, y
