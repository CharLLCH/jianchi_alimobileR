#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :get_sub.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
import gzip
import sys
from optparse import OptionParser

rule_item = 'TCReBuild/rules/item_id'
rule_user = 'TCReBuild/rules/user_id'
irf = open(rule_item,'rb')
urf = open(rule_user,'rb')
irf.readline()
urf.readline()
irlist = []
urlist = []

for i in irf.readlines():
    irlist.append(i.strip())
irf.close()
print 'item list :',len(irlist)
for u in urf.readlines():
    urlist.append(u.strip())
urf.close()
print 'user list :',len(urlist)

def get_sub(inp,outp,prob):
    inf = gzip.open(inp,'rb')
    inf.readline()
    outf = open(outp,'wb')
    outf.write('user_id,item_id\n')

    num = 0
    for line in inf.readlines():
        tmplist = line.strip().split(',')
        if float(tmplist[1]) >= prob:
            num += 1
            ids = tmplist[0].split('-')
            tmpstr = urlist[int(ids[0])] + ',' + irlist[int(ids[1])] + '\n'
            outf.write(tmpstr)
    inf.close()
    outf.close()
    print 'total predict %d items'%(num)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-t','--type',dest='type',help='pred or dev')

    (options, args) = parser.parse_args()

    if options.type == 'predict':
        inpath = 'pred_sub.gz'
        outpath = 'sub_ftrl.csv'
    else:
        print 'error'
        sys.exit(1)

    get_sub(inpath,outpath,0.7)
