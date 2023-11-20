import sys
sys.path.append('..')
from similarity_measurement import GeneralizedJaccard, EditDistanceMeasurement
from bound_filtering import BoundFiltering
from dataloader.d02_01_loader import d02_loader
from datetime import datetime
import multiprocessing

# ----------------------------------------------------------------
# Init file to save results
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M")
file_name = f"results/exp01_{formatted_datetime}.txt"


# ------------------------------description----------------------------------
def process(idx, x, data_y):
    ans = []
    print(17, "idx", idx)
    for idy, y in enumerate(data_y):
        measureFunc.input_strs(x, y)
        choosingFunc = BoundFiltering(measureFunc)
        casekey = choosingFunc()
        if casekey == 1 or (casekey == 2 and measureFunc()):
            ans.append((idx, idy))
            print((idx, idy))
    return ans

# ----------------------------------------------------------------
tokenThreshold = 0.5
characterThreshold = 0.5
measureFunc = GeneralizedJaccard(tokenThreshold, EditDistanceMeasurement, characterThreshold)
choosingFunc = BoundFiltering(measureFunc)
data_x, data_y, gt = d02_loader()

list_x = [(idx, x) for idx, x in enumerate(data_x)]
list_args = [(idx, x, data_y) for idx, x in enumerate(data_x)]
pool = multiprocessing.Pool(processes=10)
ans = pool.starmap(process, list_args)
ans02 = []
for tlist in ans:
    ans02 = ans02 + tlist

with open(file_name, 'w') as file:
    for item in ans02:
        line = str(item[0]) + " " + str(item[1]) + '\n'
        file.write(line)

        

print(ans02)