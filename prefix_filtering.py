import random
import copy
import sys


class Prefix_Filtering_Func(object):
    def __init__(self, num: int = 0) -> None:
        self.num = num
        return

    def __call__(self, lst: list[list[str]]) -> list[list[str]]:
        sys.exit("Method not implemented")


class RandomPrefixFiltering(Prefix_Filtering_Func):
    num: int
    def __init__(self, num: int = 0) -> None:
        super().__init__(self)
        self.num = num
        return

    def __call__(self, lst: list[list[str]]) -> list[list[str]]:
        """
        Filtering each element in the list, remove (num) words with random indices.

        The function will handle list deep copy by itself.
        """
        return _randomPrefixFiltering(lst=lst, num=self.num)


class NormalPrefixFiltering(Prefix_Filtering_Func):
    num: int
    def __init__(self, num: int = 0) -> None:
        super().__init__(self)
        self.num = num
        return

    def __call__(self, lst: list[list[str]]) -> list[list[str]]:
        """
        Filtering each element in the list, remove (num) words from the end.

        The function will handle list deep copy by itself.
        """
        return _prefixFiltering(lst=lst, num=self.num)


# helper function
def _prefixFiltering(lst: list[list[str]], num: int = 1) -> list[list[str]]:
    """
    Filtering each element in the list, remove (num) words from the end.

    The function will handle list deep copy by itself.
    """
    copyLst = copy.deepcopy(lst)
    return [ele[:-num] for ele in copyLst]


# helper function
def _randomPrefixFiltering(lst: list[list[str]], num: int = 1) -> list[list[str]]:
    copyLst = copy.deepcopy(lst)
    newLst = []
    for ele in copyLst:
        if num >= len(ele):
            # simply delete that string from lst
            continue
        for _ in range(num):
            ele.pop(random.randint(0, len(ele) - 1))
        newLst.append(ele)
    return newLst


if __name__ == "__main__":
    y = [
        ["b", "a", "c", "d"],
        ["d", "c", "s"],
    ]

    # Remove 1 random word from each sentence
    randomPrefixFilteringFunc = RandomPrefixFiltering()
    newList = randomPrefixFilteringFunc(y)
    print(newList)  # expected list[len = 3, len = 2]

    # Remove 1 word from the end of each sentenc
    normalPrefixFilteringFunc = NormalPrefixFiltering(2)
    newListPrefixFiltering = normalPrefixFilteringFunc(y)
    print(newListPrefixFiltering)  # expected [["b", "a"], ["d"]]

    from dataloader.d02_loader import d02_loader

    data_x, data_y, gt = d02_loader()
    normalPrefixFilteringFunc = NormalPrefixFiltering(1)
    newListPrefixFiltering = normalPrefixFilteringFunc(data_x)
    assert len(newListPrefixFiltering[0]) == len(data_x[0]) - 1

    print(newListPrefixFiltering[0])  # expected [["b", "a"], ["d"]]
    print(data_x[0])  # expected [["b", "a"], ["d"]]
