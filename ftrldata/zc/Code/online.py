import numpy as np
class Predictor:
    def __init__(self):
        pass
    def predict(self, clf, path = './Features/basic/valid.csv'):
        print 'online predict', path
        f = open(path)
        ids = []
        y = []
        
        cnt = 0
        X = []
        for line in f:
            cnt += 1
            if cnt % 100000 == 0:
                print ' ',cnt
                y_prd = clf.predict_proba(np.array(X, dtype = float))
                for yp in y_prd:
                    y.append(yp[1])
                del X
                X = []
            [id, feature] = line[0:-1].split(':')
            [user_id, item_id, item_category, day, label] = id.split(',')
            X.append(feature.split(','))
            #y.append(clf.predict_proba([x])[0][1])
            ids.append(user_id+','+item_id)
        f.close()
        y_prd = clf.predict_proba(np.array(X, dtype  = float))
        for yp in y_prd:
            y.append(yp[1])
        del X
        print cnt
        return ids, y
