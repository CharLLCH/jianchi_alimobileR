#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :gen_testset.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

from testset_item import get_testset_item

test_items = get_testset_item()

count = 0
for tmp_list in test_items:
    count += 1

print count
