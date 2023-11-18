class InvertedIndexFunc:
    def __init__(self):
        pass

    def __call__(self, lst: list[list[str]]) -> dict[str, list[int]]:
        index_dict = dict()  # type: dict[str, list[int]]
        for str_index, str in enumerate(lst):
            for word in str:
                idxx = index_dict.get(word, [])
                idxx.append(str_index)
                index_dict[word] = idxx
        return index_dict


if __name__ == "__main__":
    lst= [['lake', 'monona', 'university'],
          ['monona', 'research', 'area'],
          ['lake', 'mendota', 'monona', 'area']]
    tableIndex= InvertedIndexFunc()
    print(tableIndex(lst))

