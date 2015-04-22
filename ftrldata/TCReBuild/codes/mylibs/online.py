import numpy as np
import csv
class Predictor:
    def __init__(self):
        pass
    def predict(self, clf, path = './Features/basic/valid.csv'):
        print 'online predict', path
        f = open(path)
        reader = csv.reader(f)
        title = reader.next()

        res = []
        y = []
        
        cnt = 0
        X = []
        for line in reader:
            cnt += 1
            if cnt % 100000 == 0:
                print ' predict',cnt,'lines'
                y_prd = clf.predict_proba(np.array(X, dtype = float))
                for yp in y_prd:
                    y.append(yp[1])
                del X
                X = []

            res.append(line[:5])
            X.append(line[6:])

        y_prd = clf.predict_proba(np.array(X, dtype  = float))
        for yp in y_prd:
            y.append(yp[1])
        del X
        
        print ' ',cnt
        f.close()
        
        for i in range(len(res)):
            res[i].append(y[i])
        return res
