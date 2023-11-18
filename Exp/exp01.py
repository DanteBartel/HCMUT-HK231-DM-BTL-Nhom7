import sys
sys.path.append('..')
from similarity_measurement import GeneralizedJaccard, EditDistanceMeasurement
from bound_filtering import BoundFiltering
from dataloader.d02_loader import d02_loader

# ----------------------------------------------------------------
tokenThreshold = 0.4
characterThreshold = 0.4
measureFunc = GeneralizedJaccard(tokenThreshold, EditDistanceMeasurement, characterThreshold)
choosingFunc = BoundFiltering(measureFunc)
data_x, data_y, gt = d02_loader()


ans = []
# print(len(data_x))
# print(data_x[0])
# exit()
for idx, x in enumerate(data_x):
    print(17, "idx", idx)
    for idy, y in enumerate(data_y):
        casekey = choosingFunc(x, y)
        if casekey == 1: ans.append((idx, idy))
        elif casekey == 2 and measureFunc(x, y): ans.append((idx, idy))
print(ans)