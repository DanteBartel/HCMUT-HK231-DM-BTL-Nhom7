import sys
import os
sys.path.append(os.getcwd())
from combined_methods import PrefixFilteringMethod
from dataloader.d03_loader import d03_loader
from inverted_index import InvertedIndexFunc
from prefix_filtering import NormalPrefixFiltering
from sort import FrequentSort
from similarity_measurement import OverlapMeasurement
from evaluate import evaluate
'''
Exp/exp03.py file contain main function of data/ccer/d3 dataset
'''
def __helper__(x: list[list[str]], y: list[list[str]]):
    '''
    calc average number of words of each row in dataset.
    '''
    c = 0
    for data in [x,y]:
        for row in data:
            c += len(row)
    import math
    return int(math.floor(c/(len(x) + len(y))))

if __name__ == "__main__":
    d1, d2, gt = d03_loader()
    result_file = os.path.join(os.getcwd(), "result", "dataset_3.txt")
    import time
    
    for k in range(5,10):
        print("k = {}".format(k))
        start = time.time()
        measureFunc = OverlapMeasurement(k)
        prefixFilteringFunc = NormalPrefixFiltering(k-1)
        invertedIndexFunc  = InvertedIndexFunc()
        sortFunc = FrequentSort()
        y_hat = PrefixFilteringMethod(
            x=d1,
            y=d2,
            similarityFunc=measureFunc,
            invertedIndexFunc=invertedIndexFunc,
            prefixFilteringFunc=prefixFilteringFunc,
            sortFunc=sortFunc,
        )
        result = evaluate(y_hat, gt)
        with open(file=result_file, mode='a') as file:
            file.write("k = {}, result = {}, time = {}s\n".format(k, result, time.time() - start))
        




    # k = 5, (0.0009, 0.9991, 0.786) # k low => number false positive >> 
