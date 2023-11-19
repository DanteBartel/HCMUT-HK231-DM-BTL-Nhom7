from sort import  Sort_Func
from prefix_filtering import  Prefix_Filtering_Func
from similarity_measurement import Similarity_Measurement
from dataloader.d01_loader import d01_loader
from dataloader.d02_loader import d02_loader
from dataloader.d09_loader import d09_loader
from inverted_index import InvertedIndexFunc

def RandomFilteringMethod(
        x: list[list[str]],
        y: list[list[str]],
        similarityFunc: Similarity_Measurement,
        prefixFilteringFunc: Prefix_Filtering_Func,
        invertedIndexFunc: InvertedIndexFunc,
)-> list[tuple[int,int]]:
    # prefix filtering each sentence in dataset
    filtered_x, filtered_y = prefixFilteringFunc(x), prefixFilteringFunc(y)

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