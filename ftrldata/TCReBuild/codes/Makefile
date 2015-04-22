days = 15
indays = 3

total_progress : generat_features.py preprocessor.py revision.py
	python preprocessor.py -d $(days)
	pypy generat_features.py -d $(days) -i $(indays)
	python revision.py

gen_feature : preprocessor.py generat_features.py
	python preprocessor.py -d $(days)
	pypy generat_features.py -d $(days) -i $(indays)

train_and_test : revision.py
	python revision.py
