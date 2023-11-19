import sys
sys.path.append('..')
from similarity_measurement import GeneralizedJaccard, EditDistanceMeasurement
from bound_filtering import BoundFiltering
from dataloader.d02_loader import d02_loader

# ----------------------------------------------------------------
tokenThreshold = 0.2
characterThreshold = 0.5
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
        measureFunc.input_strs(x, y)
        choosingFunc = BoundFiltering(measureFunc)
        casekey = choosingFunc()
        if casekey == 1 or (casekey == 2 and measureFunc()):
            ans.append((idx, idy))
            print((idx, idy))
        # if idx == 2 and idy == 33: exit()
print(ans)