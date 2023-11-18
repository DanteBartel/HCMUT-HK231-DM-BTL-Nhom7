import sys


class Similarity_Measurement(object):
    def __init__(self) -> None:
        return

    def __call__(self, str_x: list[str], str_y: list[str]) -> bool:
        sys.exit("Method not implemented")


class OverlapMeasurement(Similarity_Measurement):
    threshold: int

    def __init__(self, threshold: int) -> None:
        self.threshold = threshold
        super().__init__()

    def __call__(self, str_x: list[str], str_y: list[str]) -> bool:
        set_x = set()  # type: set[str]
        for word in str_x:
            set_x.add(word)
        set_y = set()  # type: set[str]
        for word in str_y:
            set_y.add(word)
        return len(set_x.intersection(set_y)) >= self.threshold

class JascardMeasurement(Similarity_Measurement):
    threshold: int

    def __init__(self, threshold: int) -> None:
        if (threshold>= 0 and threshold <=1):
            self.threshold = threshold
            super().__init__()
        else: 
            sys.exit("Error threshold  is only in the range [0,1]")

    def __call__(self, str_x: list[str], str_y: list[str]) -> bool:
        set_x = set()  # type: set[str]
        for word in str_x:
            set_x.add(word)
        set_y = set()  # type: set[str]
        for word in str_y:
            set_y.add(word)

        intersection = len(set_x.intersection(set_y))
        combination  = len(set_x) + len(set_y) - intersection

       # print(intersection,combination)
        return intersection/combination >= self.threshold

if __name__ == "__main__":
    str_x = ["a", "b", "c"]
    str_y = ["a", "c"]
    measureFunc = JascardMeasurement(0.5)
    assert measureFunc(str_x, str_y) == True

    # str_x = ["a", "b", "c"]
    # str_y = ["a", "d"]
    # assert measureFunc(str_x, str_y) == False

    # str_x = ["a", "b", "b", "c"]
    # str_y = ["a", "d"]
    # assert measureFunc(str_x, str_y) == False
