#coding=utf-8
import paths

from mylibs.feature import *

import os
from optparse import OptionParser

def basic_feature(days):
    b = Basic()
    b.load('../data/encode/user.csv')
    b.generate('../data/divid/sub.csv','../data/features/basic/sub.csv',days)
    b.generate('../data/divid/train.csv','../data/features/basic/train.csv',days)
    b.generate('../data/divid/dev.csv','../data/features/basic/dev.csv',days)

def extend_feature(indays):
    e = Extend()
    e.load('../data/encode/user.csv')
    e.generate('../data/features/basic/sub.csv','../data/features/extend/sub.csv',indays)
    e.generate('../data/features/basic/train.csv','../data/features/extend/train.csv',indays)
    e.generate('../data/features/basic/dev.csv','../data/features/extend/dev.csv',indays)
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-d','--days',dest='days',help="days of the feature")
    parser.add_option('-i','--indays',dest='indays',help='beh indays')

    (options, args) = parser.parse_args()

    if int(options.days) > 0 and int(options.indays) > 0:
        basic_feature(int(options.days))
        extend_feature(int(options.indays))
    else:
        print 'error'
        sys.exit(1)
