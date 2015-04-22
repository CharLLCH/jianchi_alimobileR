import csv
import numpy as np

def write_file(fdir, title, contents):
    f = open(fdir, 'w')
    writer = csv.writer(f)
    writer.writerow(title)
    for c in contents:
        writer.writerow(c)
    f.close()

def read_file(fdir, has_title = True):
    print 'read file', fdir
    f = open(fdir, 'r')
    reader = csv.reader(f)
    dic = {}
    title = []
    print ' analyse title'
    if has_title:
        title = reader.next()
        for i in range(len(title)):
            dic[title[i]] = i
    contents = []
    print ' read contents'
    cnt = 0
    for line in reader:
        cnt += 1
        if cnt % 1000000 == 0:
            print ' read',cnt,'lines'
        contents.append(line)
    f.close()
    
    print ' read',cnt,'lines'
    print 'read complete!\n'
    return dic, title, contents
        
def load_train(fdir):
    print 'load train', fdir
    f = open(fdir)
    reader = csv.reader(f)
    title = reader.next()
    ids = []
    X = []
    y = []
    cnt = 0
    for line in reader:
        cnt += 1
        if cnt % 100000 == 0:
            print ' load',cnt,'lines'
        ids.append(line[:5])
        X.append(line[6:])
        y.append(line[4])
    f.close()
    print ' load', cnt, 'lines'
    print 'load train succeed!\n'
    return np.array(X, dtype = float), np.array(y, dtype = int), ids

