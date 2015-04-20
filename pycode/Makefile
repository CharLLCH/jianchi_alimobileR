
db_create : create_db.py ../util/get_item.py ../util/item.py
	time python create_db.py create

db_delete : create_db.py ../util/get_item.py ../util/item.py
	time python create_db.py delete

feat_test : feat_sql.py ../util/item.py ../util/get_item.py
	time python feat_sql.py test

feat_train : feat_sql.py ../util/item.py ../util/get_item.py
	time python feat_sql.py train

store_metrix : feat_to_metrix.py ../util/get_item.py
	time python feat_to_metrix.py

gen_vw_feat : gen_feature.py ../util/item.py ../util/get_item.py
	time python gen_feature.py -d train -t vw
	time python gen_feature.py -d test -t vw

adjust_set : gen_dataset.py ../util/get_item.py
	time pypy gen_dataset.py -d train
	time pypy gen_dataset.py -d test

gen_total_feat : gen_feature.py gen_catfeat.py ../util/item.py ../util/get_item.py
	time python gen_feature.py -d train -t normal
	time python gen_feature.py -d test -t normal

gen_train_feat : gen_feature.py gen_catfeat.py  ../util/item.py ../util/get_item.py
	time python gen_feature.py -d train -t normal
	time pypy gen_catfeat.py -d train

gen_test_feat : gen_feature.py gen_catfeat.py ../util/item.py ../util/get_item.py
	time python gen_feature.py -d test -t normal
	time pypy gen_catfeat.py -d test

predict_test : prediction.py ../util/get_item.py
	time python prediction.py -d test
	time python submit_list.py -t test

predict_pred : prediction.py ../util/get_item.py
	time python prediction.py -d pred
	time python submit_list.py -t pred

post_handler : submit_list.py ../util/get_item.py
	time python submit_list.py -t $(type)

get_all_pred : gen_feature.py gen_catfeat.py ../util/item.py ../util/get_item.py
	time python gen_feature.py -d pred -t normal
	time pypy gen_catfeat.py -d pred
	time python prediction.py -d pred
	time python submit_list.py -t pred
