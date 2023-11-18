from sort import FrequentSort, Sort_Func
from prefix_filtering import NormalPrefixFiltering, Prefix_Filtering_Func
from similarity_measurement import Similarity_Measurement, OverlapMeasurement
from dataloader.d01_loader import d01_loader
from dataloader.d02_loader import d02_loader
from dataloader.d09_loader import d09_loader
from inverted_index import InvertedIndexFunc
from evaluate import evaluate

def PrefixFilteringMethod(
    x: list[list[str]],
    y: list[list[str]],
    similarityFunc: Similarity_Measurement,
    prefixFilteringFunc: Prefix_Filtering_Func,
    invertedIndexFunc: InvertedIndexFunc,
    sortFunc: Sort_Func,
) -> list[tuple[int, int]]:
    # Sort chracter in x and y
    [sorted_x, sorted_y] = sortFunc([x, y])

    # prefix filtering each sentence in dataset
    filtered_x, filtered_y = prefixFilteringFunc(sorted_x), prefixFilteringFunc(sorted_y)

    # build inverted_index_table with filtered_y
    invertedIndex = invertedIndexFunc(filtered_y)  # type: dict[str, list[int]]

    result = []  # type: list[tuple[int,int]]

    for index_x, sentence_x in enumerate(filtered_x):
        # doing some stuff, check similarity with filtered_y

        # get candidates string from invertedIndex table
        candidate_senctence_indices = set()  # type: set[int]
        for word in sentence_x:
            candidates = invertedIndex.get(word, [])
            [candidate_senctence_indices.add(candidate) for candidate in candidates]

        # calc similarity with each candidate
        for index_y in candidate_senctence_indices:
            if similarityFunc(str_x=sentence_x, str_y=filtered_y[index_y]):
                result.append((index_x, index_y))

    return result

# Test for D01
# if __name__ == "__main__":
#     filterFunc = NormalPrefixFiltering()
#     sortFunc = FrequentSort()
#     measureFunc = OverlapMeasurement(4)
#     invertedIndexFunc = InvertedIndexFunc()
#     data_x, data_y, gt = d01_loader()
#     print(data_x[:5], data_y[:5])
#     y_hat = PrefixFilteringMethod(
#         data_x, data_y, measureFunc, filterFunc, invertedIndexFunc, sortFunc
#     )
#     top, fop, tog = evaluate(y_hat, gt)
#     print("Percentage of true predictions over all predictions: {}\nPercentage of false predictions over all prediction: {}\nPercentage of true predictions over ground truth: {}".format(top, fop, tog))


if __name__ == "__main__":
    filterFunc = NormalPrefixFiltering()
    sortFunc = FrequentSort()
    measureFunc = OverlapMeasurement(8)
    invertedIndexFunc = InvertedIndexFunc()
    data_x, data_y, gt = d09_loader()
    y_hat = PrefixFilteringMethod(
        data_x, data_y, measureFunc, filterFunc, invertedIndexFunc, sortFunc
    )
    print(y_hat)
    top, fop, tog = evaluate(y_hat, gt)
    print("Percentage of true predictions over all predictions: {}\nPercentage of false predictions over all prediction: {}\nPercentage of true predictions over ground truth: {}".format(top, fop, tog))