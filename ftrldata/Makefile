L1 = 15.0
L2 = 15.0
dropout = 1.0
n_epochs = 3
bits = 24

train : adjust_ftrl.py check_out.py
	pypy adjust_ftrl.py train -t ftrl_tr.csv -o model.gz --L1 $(L1) --L2 $(L2) --dropout $(dropout) --n_epochs $(n_epochs) --bits $(bits)
	pypy adjust_ftrl.py predict --test ftrl_de.csv -i model.gz --L1 $(L1) --L2 $(L2) --dropout $(dropout) --n_epochs $(n_epochs) --bits $(bits) -p test_sub.gz
	pypy check_out.py

predict : adjust_ftrl.py get_sub.py
	pypy adjust_ftrl.py predict --test ftrl_te.csv -i model.gz --L1 $(L1) --L2 $(L2) --dropout $(dropout) --n_epochs $(n_epochs) --bits $(bits) -p pred_sub.gz
	pypy get_sub.py -t predict
