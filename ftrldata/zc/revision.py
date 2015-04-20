from Code.data import Load
from Code.transform import Encoder
from Code.online import Predictor
from Code.Index import Dic_Builder
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier

valid_path = './Features/basic/valid.csv'
train_path = './Features/basic/train.csv'
test_path = './Features/basic/test.csv'
clf_path = './Models/clf.pkl'
result_path = './Submit/result.csv'
submit_path = './Submit/submit.csv'
rule_path = './Others/TransformRules'
def select_model():
    return RandomForestClassifier(n_estimators=10,max_depth=10,max_features='auto')
    #return LogisticRegression(penalty='l2')
    #return GradientBoostingClassifier(n_estimators=5)

def train():
    clf = select_model()
    X, y, ids = Load().load(train_path)
    print 'train'
    clf.fit(X, y)
    print 'predict'
    y_prd = clf.predict(X)
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
    f = open(clf_path, 'w')
    pickle.dump([clf], f)
    f.close()
#######################################################################
def valid():
    db = Dic_Builder('./Data/divid/valid_pos.csv')
    user_item = db.get_dic(['user_id','item_id'],[])
    ids, y = valid_predict()
    dump_pickle('./Others/valid.pkl',ids, y)
    
    score(ids, y, user_item, -0.1)
    score(ids, y, user_item, 0.4)
    score(ids, y, user_item, 0.5)
    score(ids, y, user_item, 0.6)
    score(ids, y, user_item, 0.7)

def scores():
    [ids, y] = load_pickle('./Others/valid.pkl')
  
    score(ids, y, user_item, 0.3)
    score(ids, y, user_item, 0.5)
    score(ids, y, user_item, 0.6)
    score(ids, y, user_item, 0.7)

valid_del_path = './Features/del/valid.csv'
def valid_predict():
    print 'valid'
    f = open(clf_path)
    [clf] = pickle.load(f)
    f.close()
    
    ptor = Predictor()
    ids, y = ptor.predict(clf, valid_path)

    return ids, y
def score(ids,y,user_item,limit = 0.5):
    print 'score limit:',limit
    c1 = 0
    c2 = 0
    for i in range(len(ids)):
        if y[i] > limit:
            c1 += 1
            if user_item.has_key(ids[i]):
                c2 += 1
    if c1 == 0:
        print ' p\t','error'
        print ' r\t', 0
        print ' f1\t','error'
    elif c2 == 0:
        print ' p\t',0
        print ' r\t', 0
        print ' f1\t','error'
    else:
        p = float(c2)/c1
        r = float(c2)/len(user_item)
        print ' output', c1, '\tpos_size:\t',len(user_item), '\tpredict right\t', c2
        print ' p\t', p
        print ' r\t', r
        print ' f\t', 2*p*r/(p+r)
################################################################
def submit():
    print 'submit'
    f = open(clf_path)
    [clf] = pickle.load(f)
    f.close()
    
    ptor = Predictor()
    ids, y = ptor.predict(clf, test_path)

    dump_pickle('./Others/test.pkl', ids, y)
    f.close()

    count(ids, y, limit = 0.3)
    count(ids, y, limit = 0.5)
    count(ids, y, limit = 0.6)
    count(ids, y, limit = 0.7)
    write(ids, y, 0.5)
def counts():
    [ids, y] = load_pickle('./Others/test.pkl')
    count(ids, y, limit = -0.1)
    count(ids, y, limit = 0.5)
    count(ids, y, limit = 0.6)
    count(ids, y, limit = 0.7)
def count(ids, y, limit = 0.5):
    cnt = 0
    for i in range(len(y)):
        if y[i] > limit:
            cnt += 1
    print ' pos\t', cnt,'\limit:\t',limit
def load_pickle(path):
    f= open(path)
    ids = []
    y = []
    for line in f:
        line = line[:-1].split(':')
        ids.append(line[0])
        y.append(float(line[1]))
    f.close()
    return [ids, y]
def dump_pickle(path,ids,y):
    f = open(path,'w')
    for i in range(len(ids)):
        f.write(ids[i]+':'+str(y[i])+'\n')
    f.close()
def write(ids, y, limit = 0.5):
    f = open(result_path, 'w')
    f.write('user_id,item_id\n')
    for i in range(len(y)):
        if y[i] > limit:
            f.write(ids[i]+'\n')
    f.close()
    Encoder(rule_path).decode_file(result_path, submit_path)
valid_pos = './Data/divid/valid_pos.csv'
if __name__ == '__main__':
    #train()
    #valid()
    #submit()
    [ids,y]=load_pickle('../submit.csv')
    #[ids,y]=load_pickle('../new_sub.csv')
    p_list = [0.5,0.55,0.6,0.65,0.7]
    for p in p_list:
        print p
        score(ids,y,Dic_Builder('./Data/divid/valid_pos.csv').get_dic(['user_id','item_id'],[]),p)

    #[ids, y] = load_pickle('../submit.csv')
    [ids, y] = load_pickle('../submit.csv')
    write(ids,y,0.65)
