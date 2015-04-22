import mylibs.transform
from mylibs.transform import *
from mylibs.divid import *
from mylibs.feature import *

#mylibs.transform.split_time('../data/original/user.csv', '../data/original/user_new.csv')

#mk = Maker()
#mk.make_transform_rules('../data/original/user_new.csv','../rules/',['user_id','item_id','item_category','time'])


#encoder = Encoder('../rules/',['user_id','item_id','item_category','time'])
#encoder.encode_file('../data/original/item.csv', '../data/encode/item.csv')
#decoder = Decoder('../rules/',['user_id','item_id','item_category','time'])
#decoder.decode_file('../data/encode/item.csv','../data/encode/item2.csv')
#encoder.encode_file('../data/original/user_new.csv','../data/encode/user.csv')

#Splitter().generate_dev_pos(['30'], '../data/encode/user.csv', '../data/divid/dev_pos.csv')
#Splitter().select_train(['30'], '../data/encode/user.csv','../data/divid/train.csv',15,5)
#Splitter().generate('31','../data/encode/user.csv','../data/divid/sub.csv',15,0,'../data/encode/item.csv')
#Splitter().generate('30','../data/encode/user.csv','../data/divid/dev.csv',15,0,'')
#b = Basic()
#b.load('../data/encode/user.csv')
#b.generate('../data/divid/sub.csv','../data/features/basic/sub.csv',15)
#b.generate('../data/divid/train.csv','../data/features/basic/train.csv',15)
#b.generate('../data/divid/dev.csv','../data/features/basic/dev.csv',15)
e = Extend()
e.load('../data/encode/user.csv')
e.generate('../data/features/basic/sub.csv','../data/features/extend/sub.csv',3)
e.generate('../data/features/basic/train.csv','../data/features/extend/train.csv',3)
e.generate('../data/features/basic/dev.csv','../data/features/extend/dev.csv',3)
