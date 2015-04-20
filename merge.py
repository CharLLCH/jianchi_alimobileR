#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :merge.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''
def merge(inp1,inp2,outp):
    inf1 = open(inp1,'rb')
    inf2 = open(inp2,'rb')
    outf = open(outp,'wb')

    m_set = []
    u_set = []
    
    inf2.readline()
    outf.write(inf1.readline())

    for line in inf1.readlines():
        tmp = line.strip()
        if tmp in u_set:
            pass
        else:
            u_set.append(tmp)
    inf1.close()

    for line in inf2.readlines():
        tmp = line.strip()
        if tmp in u_set:
            m_set.append(tmp)
        else:
            u_set.append(tmp)
    inf2.close()

    print len(u_set),len(m_set)

    for i in m_set:
        tmps = i+'\n'
        outf.write(tmps)

    outf.close()



if __name__ == "__main__":
    merge('19hao.csv','300ge.csv','final.csv')
