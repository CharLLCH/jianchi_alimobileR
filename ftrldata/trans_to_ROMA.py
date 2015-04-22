#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :trans_to_ROMA.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
def trans_val(value):
    if value == '0' or value == '?':
        return value
    else:
        val = int(value)
        if val > 0 and val <=5:
            return 'I'
        elif val > 5 and val <= 15:
            return 'II'
        elif val > 15 and val <= 25:
            return 'III'
        elif val > 25 and val <= 50:
            return 'IV'
        elif val > 50 and val <= 100:
            return 'V'
        elif val > 100 and val <= 200:
            return 'VI'
        elif val > 200 and val <= 500:
            return 'VII'
        elif val > 500 and val <= 1000:
            return 'VIII'
        else:
            return 'IX'

def trans_to_cat(inp,outp):
    inf = open(inp,'rb')
    outf = open(outp,'wb')

    outf.write(inf.readline())

    count = 0
    
    for line in inf.readlines():
        count += 1
        items = line.strip().split(',')
        tmp = []
        for i in range(6):
            tmp.append(items[i])
        for item in items[6:]:
            tmp.append(trans_val(item))

        tmp_str = ','.join(tmp) + '\n'
        outf.write(tmp_str)

        if count % 100000 == 0:
            print count

    inf.close()
    outf.close()

if __name__ == "__main__":
    tr_in_p = 'TCReBuild/data/features/extend/train.csv'
    te_in_p = 'TCReBuild/data/features/extend/sub.csv'
    de_in_p = 'TCReBuild/data/features/extend/dev.csv'

    tr_out = 'ftrl_tr.csv'
    te_out = 'ftrl_te.csv'
    de_out = 'ftrl_de.csv'

    trans_to_cat(tr_in_p,tr_out)
    trans_to_cat(te_in_p,te_out)
    trans_to_cat(de_in_p,de_out)
