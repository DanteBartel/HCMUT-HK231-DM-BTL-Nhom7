from similarity_measurement import Similarity_Measurement, OverlapMeasurement, JaccardMeasurement
from dataloader.d02_loader import d02_loader
from dataloader.d09_loader import d09_loader
from dataloader.d01_loader import d01_loader
from inverted_index import InvertedIndexFunc
from evaluate import evaluate

#################### FILE Run Jaccard Measurement ####################


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

def InvertedIndexMethod(
    x: list[list[str]],
    y: list[list[str]],
    similarityFunc: Similarity_Measurement,
    invertedIndexFunc: InvertedIndexFunc
    )->list[tuple[int, int]]:


    # build inverted_index_table with y
    invertedIndex = invertedIndexFunc(y)  # type: dict[str, list[int]]

    result = []  # type: list[tuple[int,int]]

    for index_x, sentence_x in enumerate(x):

        # get candidates string from invertedIndex table
        candidate_senctence_indices = set()  # type: set[int]
        for word in sentence_x:
            candidates = invertedIndex.get(word, [])
            [candidate_senctence_indices.add(candidate) for candidate in candidates]
      
        # calc similarity with each candidate
        for index_y in candidate_senctence_indices:
            if similarityFunc(str_x=sentence_x, str_y=y[index_y]):
                result.append((index_x, index_y))

    return result


   





if __name__ == "__main__":

    data_x, data_y, gt = d02_loader()
    
    invertedIndexFunc = InvertedIndexFunc()
    import time

    for i in range(1,11):
        start = time.time()
        measureFunc = JaccardMeasurement(0.1*i)
        print(f"JaccardMeasurement: Inverted Index method k={0.1*i} ")  
        result_2 = InvertedIndexMethod(data_x, data_y,measureFunc,invertedIndexFunc)
        top2, fop2, tog2 = evaluate(result_2, gt)
        print("Percentage of true predictions over all predictions: {}\nPercentage of false predictions over all prediction: {}\nPercentage of true predictions over ground truth: {}\nTime: {}".format(top2, fop2, tog2,time.time() - start))
        print("--------------------------------")
        

#     print("JaccardMeasurement: Dredging method ")  
#     result_1 = DredgingMethod(data_x, data_y,measureFunc)
#    # print(result_1)
#     top1, fop1, tog1 = evaluate(result_1, gt)
#     print("Percentage of true predictions over all predictions: {}\nPercentage of false predictions over all prediction: {}\nPercentage of true predictions over ground truth: {}".format(top1, fop1, tog1))

#     print("-----------------------------------------------------------------------------")
    
#     print("JaccardMeasurement: Inverted Index method ")  
#     result_2 = InvertedIndexMethod(data_x, data_y,measureFunc,invertedIndexFunc)
#   #  print(result_2)
#     top2, fop2, tog2 = evaluate(result_2, gt)
#     print("Percentage of true predictions over all predictions: {}\nPercentage of false predictions over all prediction: {}\nPercentage of true predictions over ground truth: {}".format(top2, fop2, tog2))

