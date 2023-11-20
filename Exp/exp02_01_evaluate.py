import sys
sys.path.append('..')
from evaluate import evaluate
from dataloader.d01_loader import d01_loader

# ----------------------------------------------------------------
data_x, data_y, gt = d01_loader()
tokenThresholds = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
for i in range(len(tokenThresholds)):
    file_name = f"results/restaurant/exp01_thresh_0.{i+1}_cT0.7.txt"
    list_of_predicts = []
    with open(file_name, 'r') as file:
        for line in file:
            words = line.strip().split()
            if len(words) >= 2:
                idx = int(words[0])
                idy = int(words[1])
                tpl = (idx, idy)
                list_of_predicts.append(tpl)
    e01, e02, e03 = evaluate(list_of_predicts, gt)
    print("Evaluate for 0.{} threshold e01 e02 e03".format(i+1), e01, e02, e03)