import sys
sys.path.append('..')
from similarity_measurement import GeneralizedJaccard, EditDistanceMeasurement
from bound_filtering import BoundFiltering
from dataloader.d02_loader import d02_loader
from datetime import datetime

# ----------------------------------------------------------------
# Init file to save results
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M")
file_name = f"results/exp01_{formatted_datetime}.txt"

# ----------------------------------------------------------------
tokenThreshold = 0.2
characterThreshold = 0.5
measureFunc = GeneralizedJaccard(tokenThreshold, EditDistanceMeasurement, characterThreshold)
choosingFunc = BoundFiltering(measureFunc)
data_x, data_y, gt = d02_loader()

with open(file_name, 'w') as file:
    ans = []
    for idx, x in enumerate(data_x):
        print(17, "idx", idx)
        for idy, y in enumerate(data_y):
            measureFunc.input_strs(x, y)
            choosingFunc = BoundFiltering(measureFunc)
            casekey = choosingFunc()
            if casekey == 1 or (casekey == 2 and measureFunc()):
                ans.append((idx, idy))
                print((idx, idy))
                line = str(idx) + " " + str(idy) + '\n'
                file.write(line)
print(ans)