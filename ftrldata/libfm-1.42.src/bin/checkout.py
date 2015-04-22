#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :checkout.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
'''
    先产生一个dev的validation的y，然后每次读取并根据概率判断就好了
'''
def get_the_valy():
    valy = open('fm_de.csv.libfm','rb')
    line = valy.readline()
    count = 0
    ylist = []
    while(line):
        ylist.append(line.strip().split(' ')[0])
        count += 1
        line = valy.readline()
    valy.close()
    print count
    print len(ylist)
    outf = open('dev_y','wb')
    outf.write('\n'.join(ylist))
    outf.close()

def get_the_ids():
    ids = open('../../TCReBuild/data/features/extend/dev.csv','rb')
    outf = open('dev_ids','wb')
    ids.readline()
    line = ids.readline()
    count = 0
    while(line):
        tmplist = line.strip().split(',')
        tmpstr = '%s-%s\n'%(tmplist[0],tmplist[1])
        count += 1
        outf.write(tmpstr)
        line = ids.readline()
    ids.close()
    outf.close()
    print count

devpos = open('/home/charch/gitwork/jianchi_alimobileR/ftrldata/TCReBuild/data/divid/dev_pos.csv','rb')
devlist = []
devpos.readline()
devline = devpos.readline()
devcount = 0
while(devline):
    tlist = devline.strip().split(',')
    devlist.append('%s-%s'%(tlist[0],tlist[1]))
    devcount += 1
    devline = devpos.readline()
devpos.close()

def check_out(p):
    inf = open('test.out','rb')
    dev = open('dev_ids','rb')
    index = 0
    count = 0
    line = inf.readline()
    while(line):
        ids = dev.readline().strip()
        if float(line.strip()) >= p:
            count += 1
            if ids in devlist:
                index += 1
        line = inf.readline()

    print '---------------------%.2f-------------------------'%(p)
    print 'Total_predicted: %d  True_pos : %d of %d'%(count,index,devcount)
    p_s = index * 1. / count
    r_s = index * 1. / devcount
    f_s = 2 * p_s * r_s / (p_s + r_s)
    print 'P_score : %.5f  R_score : %.5f  F1_score : %.5f'%(p_s,r_s,f_s)

    inf.close()
    dev.close()


if __name__ == "__main__":
    #get_the_valy()
    #get_the_ids()
    #for p in [0.5,0.6,0.7,0.75,0.8,0.85]:
    for p in [0.2,0.3,0.4]:
        check_out(p)

