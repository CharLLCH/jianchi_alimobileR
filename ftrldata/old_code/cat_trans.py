#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :cat_trans.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

def trans_val(value):
    if value == '0':
        return value
    elif value == '?':
        return value
    else:
        val = int(value)
        if val > 0 and val <= 5:
            return 'I'
        elif val > 5 and val <= 10:
            return 'II'
        elif val > 10 and val <= 20:
            return 'III'
        elif val > 20 and val <= 50:
            return 'IV'
        elif val > 50 and val <= 100:
            return 'V'
        elif val > 100 and val <= 200:
            return 'VI'
        elif val > 200 and val <= 500:
            return 'VIII'
        elif val > 500 and val <= 1000:
            return 'IX'
        else:
            return 'X'


def mark_in_cat(inpath,outpath):
    inflie = open(inpath,'rb')
    outfile = open(outpath,'wb')

    outfile.write(inflie.readline())

    count = 0
    
    for line in inflie.readlines():
        count += 1
        items = line.strip().split(',')
        tmp = []
        for i in range(5):
            tmp.append(items[i])
        for item in items[5:]:
            tmp.append(trans_val(item))

        tmp_str = ','.join(tmp) + '\n'
        outfile.write(tmp_str)

        if count % 10000 == 0:
            print count

    outfile.close()
    inflie.close()

if __name__ == "__main__":
    mark_in_cat('ftrl_tr.csv','new_tr.csv')
    mark_in_cat('ftrl_te.csv','new_te.csv')
    mark_in_cat('ftrl_pr.csv','new_pr.csv')
