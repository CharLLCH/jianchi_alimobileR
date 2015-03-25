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

    def __eq__(self,other):
        if isinstance(other,type(self)):
            result = (self.vec == other.vec)
        elif isinstance(other,type(self.vec)):
            result = (self.vec == other)
        else:
            result = NoImplemented
        return result

    def __getitem__(self,key):
        "如果有key返回key，否则返回0"
        return self.vec.get(key,0)

    def __mul__(self,num):
        "数乘，__class__再创建一个初始化类"
        return self.__class__({key: val*num for key,val in self.vec.items()})

    def __rmul__(self,num):
        return self.__class__({key: val*num for key,val in self.vec.items()})
    
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

    def norm(self):
        "获得向量的长度"
        n = self.dot(self)
        return math.sqrt(sum(n.values()))


class Test(unittest.TestCase):
    "单元测试"
    def setUp(self):
        pass

    def testInit(self):
        cal_vec1 = cal_vector({1:2})
        self.assertEqual(cal_vec1.vec,{1:2})

    def testGetitem(self):
        cal_1 = cal_vector({'a':2,'c':3})
        self.assertEqual(cal_1['a'],2)

    def testMul(self):
        vec_1 = cal_vector({'a':2,'c':3})
        self.assertEqual(vec_1*2,{'a':4,'c':6})

    def testRmul(self):
        vec_1 = cal_vector({'a':2,'c':3})
        self.assertEqual(3*vec_1,{'a':6,'c':9})

    def testDot(self):
        vec_1 = cal_vector({'a':2,'c':3})
        vec_2 = cal_vector({'a':3,'b':2})

        self.assertEqual(vec_1.dot(vec_2),{'a':6})

    def testNorm(self):
        vec_1 = cal_vector({'a':2,'c':3})

        self.assertEqual(vec_1.norm(),math.sqrt(2*2+3*3))


if __name__ == "__main__":
    unittest.main()
