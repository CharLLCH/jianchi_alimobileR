#coding=utf-8
import paths
from mylibs.transform import *
import mylibs.transform
from mylibs.divid import *

from optparse import OptionParser
import sys
import logging

def divid_time():
    mylibs.transform.split_time('../data/original/user.csv', '../data/original/user_new.csv')

def make_rule():
    mk = Maker()
    mk.make_transform_rules('../data/original/user_new.csv','../rules/',['user_id','item_id','item_category','time'])



def transform():
    encoder = Encoder('../rules/',['user_id','item_id','item_category','time'])
    encoder.encode_file('../data/original/item.csv', '../data/encode/item.csv')
    encoder.encode_file('../data/original/user_new.csv','../data/encode/user.csv')

def divid(days):
    Splitter().generate_dev_pos(['30'], '../data/encode/user.csv', '../data/divid/dev_pos.csv')
    Splitter().select_train(['30'], '../data/encode/user.csv','../data/divid/train.csv',days,5)
    Splitter().generate('31','../data/encode/user.csv','../data/divid/sub.csv',days,0,'../data/encode/item.csv')
    Splitter().generate('30','../data/encode/user.csv','../data/divid/dev.csv',days,0,'')

if __name__ == '__main__':
    divid_time()
    make_rule()
    transform()
    
    parser = OptionParser()
    
    parser.add_option('-d','--days',dest='days',help='产生的天数')

    (options, args) = parser.parse_args()

    #divid(15)
    if int(options.days) > 0:
        divid(int(options.days))
    else:
        print 'error..'
        sys.exit(1)
