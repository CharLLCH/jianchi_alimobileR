from Code.transform import Rule
from Code.transform import *

from Code.divid import Splitter

from Code.feature import DaysFeature
from Code.feature import Cross
from Code.feature import Combine
original_user_csv_path = './Data/original/user_new.csv'
original_item_csv_path = './Data/original/item_new.csv'
encode_user_csv_path = './Data/encode/user.csv'
encode_item_csv_path = './Data/encode/item.csv'
rule_path = './Others/TransformRules/'

divid_path = './Data/divid/'
divid_test_csv_path = './Data/divid/test.csv'
divid_valid_csv_path = './Data/divid/valid.csv'
divid_train_csv_path = './Data/divid/train.csv'

global_feature_path = './Features/global/'
feature_train_csv_path = './Features/train/train.csv'
feature_valid_csv_path = './Features/valid/valid.csv'
feature_test_csv_path = './Features/test/test.csv'
feature_train_del_path = './Features/del/train.csv'
feature_valid_del_path = './Features/del/valid.csv'
feature_test_del_path = './Features/del/test.csv'
feature_train_basic_path = './Features/basic/train.csv'
feature_valid_basic_path = './Features/basic/valid.csv'
feature_test_basic_path = './Features/basic/test.csv'

feature_day = 30
valid_time = '30'
test_time = '31'
neg_scale = 4
valid_pos_path = './Data/divid/valid_pos.csv'
def transform():
    Rule().generate(original_user_csv_path, rule_path)
    encoder = Encoder(rule_path)
    encoder.encode_file(original_user_csv_path, encode_user_csv_path)
    encoder.encode_file(original_item_csv_path, encode_item_csv_path)

def divid():
    splitter = Splitter()
    #splitter.generate_valid_pos(valid_time,encode_user_csv_path, valid_pos_path)
    #splitter.generate_valid(valid_time,encode_user_csv_path,divid_valid_csv_path,feature_day)
    #splitter.generate_test(test_time,encode_user_csv_path,encode_item_csv_path,divid_test_csv_path,feature_day)
    splitter.select_train(valid_time,encode_user_csv_path,divid_train_csv_path,neg_scale)

def feature():
    #Global().generate(encode_user_csv_path, global_feature_path)
    df = DaysFeature()
    df.load_user(encode_user_csv_path)
    df.generate('user_id', './Features/global/user_id.csv')
    df.generate('item_id', './Features/global/item_id.csv')
    df.generate('item_category', './Features/global/item_category.csv')
    #crs = Cross()
    #crs.load(encode_user_csv_path)
    #crs.cross_features(divid_train_csv_path,feature_train_basic_path,feature_train_del_path,30)
    #crs.cross_features(divid_valid_csv_path,feature_valid_basic_path,feature_valid_del_path,30)
    #crs.cross_features(divid_test_csv_path,feature_test_basic_path,feature_test_del_path,30)
    #crs.release()
if __name__ == '__main__':
    #transform()
    #divid()
    feature()
