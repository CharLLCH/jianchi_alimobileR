from mylibs.transform import *
from mylibs.online import *
import mylibs.models
import mylibs.myio
import paths

class Submit:
    def predict(self, ddir, clf_path):
        clf = mylibs.models.load(clf_path)
        ptor = Predictor()
        self.res = ptor.predict(clf, ddir)
    def save_proba(self, fdir):
        title = ['user_id','item_id','item_catgory','time','label','proba']
        mylibs.myio.write_file(fdir, title, self.res)
    def load_proba(self, fdir):
        dic, title, self.res = mylibs.myio.read_file(fdir)

    def get_pos(self, l):
        pos = []
        for sample in self.res:
            [user_id, item_id, item_category, time, label, proba] = sample
            if float(proba) > l:
                pos.append(sample)
        self.quick_sort(0,len(pos)-1, pos)
        print ' output size =', len(pos)
        return pos
    
    def quick_sort(self, s, e, pos):
        if s >= e:
            return
        selected = pos[s]
        m = s
        p = m + 1
        while p <= e:
            if float(pos[p][-1]) > float(selected[-1]):
                pos[m] = pos[p]
                m += 1
                pos[p] = pos[m]
            p += 1
        pos[m] = selected
        self.quick_sort(s, m-1, pos)
        self.quick_sort(m+1, e, pos)
    
    def submit(self, fdir, limit):
        title = ['user_id','item_id']
        pos = self.get_pos(limit)
        res = []
        for p in pos:
            res.append(p[:2])
        tdir = '../submits/tmp.csv'
        mylibs.myio.write_file(tdir, title, res)
        Decoder('../rules/',['user_id','item_id','item_category', 'time']).decode_file(tdir, fdir)

sub_final = '../data/features/extend/sub.csv'
sub_result = '../data/results/sub.csv'

if __name__ == '__main__':
    submit = Submit()
    submit.predict(sub_final, paths.clf)
    submit.save_proba(sub_result)
    #submit.load_proba(sub_result)
    submit.submit('../submits/submit.csv',0.63)
