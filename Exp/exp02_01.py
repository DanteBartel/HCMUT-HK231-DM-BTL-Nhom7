import sys
sys.path.append('..')
from similarity_measurement import GeneralizedJaccard, EditDistanceMeasurement
from bound_filtering import BoundFiltering
from dataloader.d01_loader import d01_loader
from datetime import datetime
import multiprocessing
import time
# ----------------------------------------------------------------
# Init file to save results
# current_datetime = datetime.now()
# formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M")
# file_name = f"results/exp01_{formatted_datetime}.txt"


# ------------------------------description----------------------------------
def process(idx, x, data_y):
    ans = []
    # print(19, "idx", idx)
    for idy, y in enumerate(data_y):
        measureFunc.input_strs(x, y)
        choosingFunc = BoundFiltering(measureFunc)
        casekey = choosingFunc()
        if casekey == 1 or (casekey == 2 and measureFunc()):
            ans.append((idx, idy))
            # print((idx, idy))
    return ans

# ----------------------------------------------------------------
tokenThresholds = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
for i in range(len(tokenThresholds)):
    file_name = f"results/restaurant/exp01_thresh_0.{i+1}_cT0.7.txt"
    tokenThreshold = tokenThresholds[i]
    characterThreshold = 0.7
    measureFunc = GeneralizedJaccard(tokenThreshold, EditDistanceMeasurement, characterThreshold)
    choosingFunc = BoundFiltering(measureFunc)
    data_x, data_y, gt = d01_loader()

    start_time = time.time()
    list_x = [(idx, x) for idx, x in enumerate(data_x)]
    list_args = [(idx, x, data_y) for idx, x in enumerate(data_x)]
    pool = multiprocessing.Pool(processes=8)
    ans = pool.starmap(process, list_args)
    ans02 = []
    for tlist in ans:
        ans02 = ans02 + tlist
    period = time.time()-start_time
    with open(file_name, 'w') as file:
        for item in ans02:
            line = str(item[0]) + " " + str(item[1]) + '\n'
            file.write(line)
    print("Time of loop {}: {}s".format(i+1,period))