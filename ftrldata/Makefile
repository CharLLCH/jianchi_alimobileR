L1 = 1.0
L2 = 1.0
dropout = 1
n_epochs = 3
bits = 23

train : adjust_ftrl.py
	pypy adjust_ftrl.py train -t ftrl_tr.csv -o model.gz --L1 $(L1) --L2 $(L2) --dropout $(dropout) --n_epochs $(n_epochs) --bits $(bits)

test : adjust_ftrl.py
	pypy adjust_ftrl.py predict --test ftrl_te.csv -i model.gz --L1 $(L1) --L2 $(L2) --dropout $(dropout) --n_epochs $(n_epochs) --bits $(bits) -p test_sub.gz

predict : adjust_ftrl.py
	pypy adjust_ftrl.py predict --test ftrl_pr.csv -i model.gz --L1 $(L1) --L2 $(L2) --dropout $(dropout) --n_epochs $(n_epochs) --bits $(bits) -p pred_sub.gz

test_submit : test_sub.py
	python test_sub.py

pred_submit : pred_sub.py
	python pred_sub.py

new : adjust_ftrl.py
	pypy adjust_ftrl.py train -t new_tr.csv -o newmodel.gz --L1 $(L1) --L2 $(L2) --dropout $(dropout) --n_epochs $(n_epochs) --bits $(bits)
	pypy adjust_ftrl.py predict --test new_te.csv -i newmodel.gz --L1 $(L1) --L2 $(L2) --dropout $(dropout) --n_epochs $(n_epochs) --bits $(bits) -p test_sub.gz
	python test_sub.py

new_predict : adjust_ftrl.py
	pypy adjust_ftrl.py predict --test new_pr.csv -i newmodel.gz --L1 $(L1) --L2 $(L2) --dropout $(dropout) --n_epochs $(n_epochs) --bits $(bits) -p pred_sub.gz
	python pred_sub.py
