#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :cal_vector.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

from copy import deepcopy
import unittest
import math

class cal_vector:
    def __init__(self,in_dict={}):
        self.vec = deepcopy(in_dict)

    def keys(self):
        return set(self.vec.keys())

    def values(self):
        return self.vec.values()

    def get_item(self,key):
        "如果有key返回key，否则返回0"
        return self.vec.get(key,0)

    def num_mul(self,num):
        "__class__再创建一个初始化类"
        return self.__class__({key: val*num for key,value in self.vec.items()})
    
    def dot(self,other):
        tmp_d = {}
        for key in self.vec:
            other_val = other.vec.get(key)
            if other_val == None:
                pass
            else:
                val_self = self.vec.get(key)
                tmp_d[key] = val_self * other_val

        return self.__class__(tmp_d)
