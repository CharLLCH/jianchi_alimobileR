#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :trans_to_sub.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
import gzip

devp = 'TCReBuild/data/divid/dev_pos.csv'
infile = open(devp,'rb')
infile.readline()
devlist = []
for line in infile.readlines():
    tlist = line.strip().split(',')
    devlist.append('%s-%s'%(tlist[0],tlist[1]))
infile.close()

#get the devposdict
def check_out(inp,outp,prob):
    inf = gzip.open(inp,'rb')
    #outf = open(outp,'wb')
    inf.readline()
    #outf.write('user_id,item_id\n')

    t_num = 0
    p_num = 0
    for line in inf.readlines():
        tmplist = line.strip().split(',')
        if float(tmplist[1]) >= prob:
            t_num += 1
            #ids = tmplist[0].split('-')
            #tmpstr = ids[0] + ',' + ids[1] + '\n'
            #outf.write(tmpstr)
            if tmplist[0] in devlist:
                p_num += 1
    inf.close()
    #outf.close()

    if t_num == 0:
        print 'prob too large.'
        return 
    p_score = p_num * 1. / t_num
    r_score = p_num * 1. / len(devlist)
    if p_score == 0.0 or r_score == 0.0:
        print 'no true'
        return
    else:
        f_score = 2 * p_score * r_score / (p_score + r_score)

    print "Based:%.2f-> P : %.5f -> R : %.5f -> F1 : %.5f -> N : %d -> T/P : %d/%d"%(prob,p_score,r_score,f_score,t_num,p_num,len(devlist))

if __name__ == "__main__":
    inpath = 'test_sub.gz'
    outpath = 'submit_ftrl.csv'

    for p in [0.5,0.55,0.6,0.65,0.7,0.75,0.8]:
        check_out(inpath,outpath,p)
