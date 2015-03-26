#!/usr/bin/python
#coding=utf-8

'''
**************************
 * File Name :sim_func.py
 * Author:Charlley88
 * Mail:charlley88@163.com
**************************
'''

import logging
from abc import ABCMeta, abstractmethod

# 相似度函数的抽象类
class abstract_sim:
    __metaclass__ == ABCMeta

    #计算两个向量的相似度
    @abstractmethod
    def sim(self):
        pass


# 正常商品历史相似度
class vec_cos_sim(abstract_sim):
    def sim(self,vec1,vec2):
        if type(vec1) != type(vec2):
            logging.ERROR("item_sim error..")
        else:

            norm1 = vec1.norm()
            norm2 = vec2.norm()

            dot_sum = vec1.dot(vec2)

            tmp_sum = sum(dot_sum.values())
            return tmp_sum*1.0 / (norm1 * norm2)


# 整体相似度，将各种相似度整合起来
class user_sim(abstract_sim):
    def __init__(self):
        self.ui_sim = vec_cos_sim()

    def sim(self,user1,user2):
        if type(user1) != type(user2):
            logging.ERROR("type is not match.")

        else:
            uisimilarity = self.ui_sim.sim(user1.item_feat,user2.item_feat)
            utsimilarity = self.ui_sim.sim(user1.time_feat,user2.time_feat)

            return uisimilarity+utsimilarity/2.0
