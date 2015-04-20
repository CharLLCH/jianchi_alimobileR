import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
class Load:
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
