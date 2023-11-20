import sys
sys.path.append('..')
from evaluate import evaluate
from dataloader.d02_01_loader import d02_loader

# ----------------------------------------------------------------
file_name = "results/exp01_20231120_1153.txt"
data_x, data_y, gt = d02_loader()

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
print("e01 e02 e03", e01, e02, e03)