#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :transform.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
from optparse import OptionParser

devp = '/home/charch/gitwork/jianchi_alimobileR/ftrldata/TCReBuild/data/divid/dev_pos.csv'
infile = open(devp,'rb')
infile.readline()
devlist = []
for line in infile.readlines():
    tlist = line.strip().split(',')
    devlist.append('%s-%s'%(tlist[0],tlist[1]))
infile.close()


def trans(inp,outp,flags):
    inf = open(inp,'rb')
    outf = open(outp,'wb')
    line = inf.readline()

    count = 0
    while(line):
        line = inf.readline()
        if(line):
            count += 1
            tmplist = line.strip().split(',')
            if flags == 'train':
                tmpstr = tmplist[4] + ' c:%s'%(tmplist[2])
            elif flags == 'test':
                tmpstr = '-1' + ' c:%s'%(tmplist[2])
            else:
                uistr = '%s-%s'%(tmplist[0],tmplist[1])
                if uistr in devlist:
                    tmpstr = '1' + ' c:%s'%(tmplist[2])
                else:
                    tmpstr = '0' + ' c:%s'%(tmplist[2])
            tmpval = []
            for index in range(len(tmplist[6:])):
                if tmplist[6+index] != '0':
                    tmpstr += ' %s:%s'%(index,tmplist[6+index])
            tmpstr += '\n'
            outf.write(tmpstr)
            if count % 100000 == 0:
                print count
        else:
            print count
            inf.close()
            outf.close()
            break
    
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-s','--sour',dest='sour',help='source')
    parser.add_option('-d','--dest',dest='dest',help='destination')
    parser.add_option('-t','--type',dest='type',help='type')

    (options, args) = parser.parse_args()

    trans(options.sour,options.dest,options.type)
