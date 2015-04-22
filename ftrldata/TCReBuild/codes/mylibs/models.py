import pickle
def load(fdir):
    f = open(fdir)
    [clf] = pickle.load(f)
    f.close()
    return clf

def save(fdir, clf):
    f = open(fdir, 'w')
    pickle.dump([clf], f)
    f.close()
