from mylibs.transform import *
from mylibs.online import *
from mylibs.index import *
import mylibs.myio
import mylibs.models

import paths
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier

import math

train_final = '../data/features/extend/train.csv'
class Train:
    def select_dataset(self, path):
        self.ddir = path
    def select_model(self):
        print 'select model'
        #return LogisticRegression()#penalty = 'l2', C=0.3)
        #return GradientBoostingClassifier(n_estimators=21,max_depth=5,loss='deviance')
        self.clf = RandomForestClassifier(n_estimators=35,max_depth = 13, max_features='auto',n_jobs=2)

    def train(self, clf_path):
        X, y, ids = mylibs.myio.load_train(self.ddir)
        print 'train'
        self.clf.fit(X, y)
        self.evaluation(X, y)
        mylibs.models.save(clf_path, self.clf)
    
    def evaluation(self, X, y):
        print 'evalution'
        y_prd = self.clf.predict(X)
        m = [[0,0],[0,0]]
        for i in range(len(y)):
            m[y_prd[i]][y[i]] += 1
        print '          \t','real 0\t','real 1'
        print ' predict 0\t',m[0][0],'\t', m[0][1]
        print ' predict 1\t',m[1][0],'\t', m[1][1]
        p = float(m[1][1])/(m[1][1]+m[1][0])
        r = float(m[1][1])/(m[1][1]+m[0][1])
        f1 = 2*r*p/(p+r)
        print ' p\t',p
        print ' r\t',r
        print ' f1\t',f1
#############################################3
#######################################################################
dev_final = '../data/features/extend/dev.csv'
dev_result = '../data/results/dev.csv'
class Dev:
    def predict(self, ddir, clf_path):
        clf = mylibs.models.load(clf_path)
        ptor = Predictor()
        self.res = ptor.predict(clf, ddir)

    def save_proba(self, fdir):
        title = ['user_id','item_id','item_catgory','time','label','proba']
        mylibs.myio.write_file(fdir, title, self.res)
    def load_proba(self, fdir):
        dic, title, self.res = mylibs.myio.read_file(fdir)
    def evalution(self, limit, dev_pos):
        for l in limit:
            pos = []
            pos.extend(self.get_pos(l))
            print 'limit =', l, '\toutput size =', len(pos), '\tpos size =', len(dev_pos)
            self.__evalution__(pos, dev_pos)
    def get_pos(self, l):
        pos = set()
        for sample in self.res:
            [user_id, item_id, item_category, time, label, proba] = sample
            if float(proba) > l:
                pos.add(user_id+','+item_id)
        return pos
    def __evalution__(self, pos, dev_pos):
        print ' dev evalution:'
        c1 = len(pos)
        c2 = len(dev_pos)
        c = 0.0
        for i in pos:
            if dev_pos.has_key(i):
                c += 1
        if c1 == 0:
            print '  precision = error'
        else:
            print '  precision =', c/c1
        if c2 == 0:
            print '  recall    = error'
        else:
            print '  recall    =', c/c2
        if c1 + c2 == 0:
            print '  f1 score  = error'
        else:
            print '  f1 score  =', 2*c/(c1+c2)
        print ''
################################
def train():
    t = Train()
    t.select_model()
    t.select_dataset(train_final)
    t.train(paths.clf)
def dev():
    d = Dev()
    d.predict(dev_final, paths.clf)
    d.save_proba(dev_result)
    #d.load_proba(dev_result)
    d.evalution([-0.1,0.3,0.5,0.53,0.56,0.6,0.63,0.67,0.7], DicBuilder('../data/divid/dev_pos.csv').get_dic(['user_id','item_id'],[]))

if __name__ == '__main__':
    train()
    dev()
