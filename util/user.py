#coding=utf-8

'''
    定义一个user类用来存放用户信息，从而计算user-user
    现在的情况是，我统计出来的是按照uid和所有特征行存
    然后要将他转化成用cal_vector形式存放的dict，所以在
    初始化这需要一个转化函数

    还是说我直接不要存成行形式，直接用dict存就好了

'''

from cal_vector import cal_vector

class user(object): 
    def __init__(self,u_id,i_vec = {},t_vec = {}):
        self.user_id = u_id
        self.item_feat = cal_vector(i_vec)
        self.time_feat = cal_vector(t_vec)
