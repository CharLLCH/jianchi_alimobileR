
db_create : create_db.py ../util/get_item.py ../util/item.py
	time python create_db.py create

db_delete : create_db.py ../util/get_item.py ../util/item.py
	time python create_db.py delete

feat_test : feat_sql.py ../util/item.py ../util/get_item.py
	time python feat_sql.py test

feat_train : feat_sql.py ../util/item.py ../util/get_item.py
	time python feat_sql.py train

feat : feat_sql.py ../util/item.py ../util/get_item.py
	time python feat_sql.py train -O
	time python feat_sql.py test -O

store_metrix : feat_to_metrix.py ../util/get_item.py
	time python feat_to_metrix.py

predict : prediction.py ../util/get_item.py
	time python prediction.py
