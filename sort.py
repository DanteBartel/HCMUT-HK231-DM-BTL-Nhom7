# def SortInvertedIndex(invertedIndex:dict[str,list[int]]) -> dict[str,list[int]]:
#     '''
#         Sort inverted index, return sorted dict in descending order based on len of index list
#     '''
#     return {k: v for k, v in reversed(sorted(invertedIndex.items(), key=lambda item: len(item[1])))}


import sys
import copy


class Sort_Func(object):
    def __init__(self) -> None:
        return

    def __call__(
        self, dataset: list[list[list[str]]], ascending: bool = True
    ) -> list[list[list[str]]]:
        sys.exit("Method not implemented")


class FrequentSort(Sort_Func):
    def __init__(self) -> None:
        super().__init__()

    def __call__(
        self, dataset: list[list[list[str]]], ascending: bool = True
    ) -> list[list[list[str]]]:
        """
        Sort the dataset by the frequency of each word.

        The result is a dataset in which each sentence has been reordered by word frequency

        The function will handle list deep copy by itself.
        """
        datasetCopy = copy.deepcopy(dataset)
        return _sortWithFrequent(dataset=datasetCopy, ascending=ascending)

# dataset = [
#     [
#         ['apple', 'banana', 'orange'],
#         ['grape', 'kiwi'],
#         ['banana', 'orange']
#     ],
#     [
#         ['apple', 'strawberry'],
#         ['kiwi', 'orange'],
#         ['strawberry', 'grape', 'banana']
#     ]
# ]
def _frequent(dataset: list[list[list[str]]]) -> dict[str, int]:
    frequent_dict = dict()  # type:dict[str,int]
    for lst in dataset:
        for str in lst:
            for word in str:
                frequent_dict[word] = frequent_dict.get(word, 0) + 1
    return frequent_dict


def _sortWithFrequent(
    dataset: list[list[list[str]]], ascending: bool = True
) -> list[list[list[str]]]:
    """
    Sort the dataset by the frequency of each word.

    The result is a dataset in which each sentence has been reordered by word frequency

    The function will handle list deep copy by itself.
    """
    frequent = _frequent(dataset=dataset)
    [
        [
            ele.sort(
                key=lambda x: frequent[x] if x in frequent.keys() else 1,
                reverse=not ascending,
            )
            for ele in lst
        ]
        for lst in dataset
    ]
    return dataset


class InvertedIndexBasedSort(Sort_Func):
    invertedIndex: dict[str, list[int]]

    def __init__(
        self,
        invertedIndex: dict[str, list[int]],
    ) -> None:
        self.invertedIndex = invertedIndex
        super().__init__()

    def __call__(
        self,
        dataset: list[list[list[str]]],
        ascending: bool = True,
    ) -> list[list[list[str]]]:
        """
        Sort each element of the list in ascending order of frequency from the inverted index.

        The result is a dataset in which each sentence has been reordered by word frequency

        The function will handle list deep copy by itself.
        """
        datasetCopy = copy.deepcopy(dataset)
        return [
            _sortWithSortedInvertedIndex(lst, self.invertedIndex, ascending)
            for lst in dataset
        ]


def _sortWithSortedInvertedIndex(
    lst: list[list[str]],
    invertedIndex: dict[str, list[int]],
    ascending: bool = True,
) -> list[list[str]]:
    # sortedID = SortInvertedIndex(invertedIndex=invertedIndex)
    #  loop in list and sort
    [
        e.sort(
            key=lambda x: len(invertedIndex[x]) if x in invertedIndex.keys() else 0,
            reverse=not ascending,
        )
        for e in lst
    ]
    # for i in range(len(lst)):
    #     lst[i].sort(key=lambda x: len(invertedIndex[x]))
    return lst


# Test for sort functions
if __name__ == "__main__":
    # x = [
    #     ["b", "c"],
    #     ["a", "b"],
    # ]
    # y = [
    #     ["b", "a"],
    #     ["d", "c", "a", "b"],
    # ]
    # invertedIndex = {
    #     "a": [1],
    #     "b": [0, 1],
    #     "c": [1],
    # }

    # # Sort with inverted index
    # invertedIndexSortFunc = InvertedIndexBasedSort(invertedIndex)
    # [sortedLst] = invertedIndexSortFunc(dataset=[x])

    # print(sortedLst)  # exptected = [["c", "b"], ["a", "b"]]

    # # Sort the dataset by the frequency of each word.
    # # The result is a dataset in which each sentence has been reordered by ascending word frequency
    # frequentSortFunc = FrequentSort()
    # [sortedX, sortedY] = frequentSortFunc(dataset=[x, y])
    # print(sortedX)  # expected [["c",  "b"], ["a", "b"]]
    # print(sortedY)  # expected [["a", "b"], ["d", "c", "a", "b"]]

    from dataloader.d02_loader import d02_loader

    data_x, data_y, gt = d02_loader()
    frequentSortFunc = FrequentSort()
    [sortedX, sortedY] = frequentSortFunc(dataset=[data_x, data_y])
    print(sortedX)  # expected [["c",  "b"], ["a", "b"]]
    print(sortedY)  # expected [["a", "b"], ["d", "c", "a", "b"]]
