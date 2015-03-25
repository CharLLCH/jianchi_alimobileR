#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :read_conf.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

import sys

def config(fn):
    with open(fn,'rb') as infile:
        result = {}
        for line in infile.readlines():
            if len(line) < 4 or line[0] == '#':
                pass
            else:
                sp = line.split()
                result[sp[0]] = sp[2]
    infile.close()
    return result
