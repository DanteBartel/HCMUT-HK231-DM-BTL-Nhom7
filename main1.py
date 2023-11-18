from similarity_measurement import Similarity_Measurement, OverlapMeasurement, JascardMeasurement
from dataloader.d02_loader import d02_loader
from inverted_index import InvertedIndexFunc

#################### FILE Run Jascard Measurement ####################


# Dredging method

def DredgingMethod( 
    x: list[list[str]],
    y: list[list[str]],
    similarityFunc: Similarity_Measurement
    )->list[tuple[int, int]]:

    result = [] # type: list[tuple[int,int]]

    for index_x, sentence_x in enumerate(x):
        for index_y, sentence_y in enumerate(y):
            if similarityFunc(str_x=sentence_x, str_y=sentence_y):
                result.append((index_x, index_y))
                
    return result


# Inverted Index method


   





if __name__ == "__main__":
    # filterFunc = NormalPrefixFiltering()
    # sortFunc = FrequentSort()
    # measureFunc = OverlapMeasurement(10)
    # invertedIndexFunc = InvertedIndexFunc()
    # data_x, data_y, gt = d02_loader()
    # y_hat = PrefixFilteringMethod(
    #     data_x, data_y, measureFunc, filterFunc, invertedIndexFunc, sortFunc
    # )
    # print(y_hat)




    data_x, data_y, gt = d02_loader()
    measureFunc = JascardMeasurement(0.25)  
    result_1 = DredgingMethod(data_x, data_y,measureFunc)
    print(len(result_1), result_1)
 
