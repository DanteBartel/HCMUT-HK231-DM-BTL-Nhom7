import sys
import numpy as np
from scipy.optimize import linear_sum_assignment


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
    

class EditDistanceMeasurement(Similarity_Measurement):
    threshold: float

    def __init__(self, threshold: float) -> None:
        self.threshold = threshold
        super().__init__()

    def __call__(self, str_x: list[str], str_y: list[str]) -> bool:
        s = self.score(str_x, str_y)
        return s >= self.threshold
    
    def score(self, str_x: list[str], str_y: list[str]) -> float:
        d = self._d(str_x, str_y)
        s = 1 - (d / max(len(str_x), len(str_y)))
        return s
    
    def _d(self, x: list[str], y: list[str]) -> bool:
        len_str1 = len(x) + 1
        len_str2 = len(y) + 1

        # Initialize a matrix to store the edit distances
        matrix = [[0 for _ in range(len_str2)] for _ in range(len_str1)]

        # Initialize the matrix with values representing the cost of editing
        for i in range(len_str1):
            matrix[i][0] = i
        for j in range(len_str2):
            matrix[0][j] = j

        # Populate the matrix with edit distances
        for i in range(1, len_str1):
            for j in range(1, len_str2):
                cost = 0 if x[i - 1] == y[j - 1] else 1
                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,      # Deletion
                    matrix[i][j - 1] + 1,      # Insertion
                    matrix[i - 1][j - 1] + cost  # Substitution
                )

        # The bottom-right cell contains the edit distance
        return matrix[len_str1 - 1][len_str2 - 1]


class GeneralizedJaccard(Similarity_Measurement):
    threshold: float
    alpha: float
    sub_sm: Similarity_Measurement
    sm_edges: list[dict[int, int, float]]
    lx: int
    ly: int

    def __init__(self, threshold: float, sub_sm: Similarity_Measurement, alpha: float = 0.5) -> None:
        self.threshold = threshold
        self.alpha = alpha
        self.sub_sm = sub_sm(alpha)
        self.sm_edges = None
        super().__init__()

    def __call__(self) -> bool:
        assert self.sm_edges is not None, "There are no strings, please use the input_strs method before call."
        score = self.score()
        return score >= self.threshold
    
    def input_strs(self, str_x: list[str], str_y: list[str]):
        """
            Create edges using a Similarity Measurement that comparing each word with each other
        """
        sm_edges = []
        # Step 1: Calculate similarity score
        for i in range(len(str_x)):
            for j in range(len(str_y)):
                sm_edges.append({
                    "idx": i,
                    "idy": j,
                    "sm_score": self.sub_sm.score(str_x[i], str_y[j])
                })
        # Step 2: filter the scores with alpha threshold
        sm_edges = [edge for edge in sm_edges if edge["sm_score"] >= self.alpha]
        self.sm_edges = sm_edges
        self.lx = len(str_x)
        self.ly = len(str_y)
    
    def score(self) -> float:
        # Step 3: Find the maximum-weight matching
        sm_m_edges = self.max_weight_matching(self.sm_edges)
        # Step 4: Calculate score
        score_m = 0
        for edge in sm_m_edges:
            score_m += edge["sm_score"]
        score = score_m/(self.lx+self.ly-len(sm_m_edges))
        return score
    
    def bound(self) -> tuple[float, float]:
        assert self.sm_edges is not None, "There are no strings, please use the input_strs method before call."
        s1, s2 = self._highest_edges()
        union, intersect = self._union_intersect_edges(s1, s2)
        sum_edges_union = sum([edge["sm_score"] for edge in union])
        sum_edges_intersect = sum([edge["sm_score"] for edge in intersect])
        ub = sum_edges_union / (self.lx + self.ly - len(union))
        lb = sum_edges_intersect / (self.lx + self.ly - len(intersect))
        return ub, lb
    
    def _highest_edges(self) -> tuple[list[dict], list[dict]]:
        max_x_edges = [None for _ in range(self.lx)]
        max_y_edges = [None for _ in range(self.ly)]
        for edge in self.sm_edges:
            idx, idy = edge["idx"], edge["idy"]
            # Xét x
            if max_x_edges[idx] is None or edge["sm_score"] > max_x_edges[idx]["sm_score"]:
                max_x_edges[idx] = edge.copy()
            # Xét y
            if max_y_edges[idy] is None or edge["sm_score"] > max_y_edges[idy]["sm_score"]:
                max_y_edges[idy] = edge.copy()
        max_x_edges = [edge for edge in max_x_edges if edge is not None]
        max_y_edges = [edge for edge in max_y_edges if edge is not None]
        return max_x_edges, max_y_edges
    
    def _union_intersect_edges(self, s1: list[dict], s2: list[dict]) -> tuple[list[dict], list[dict]]:
        ans1 = {tuple(d.items()) for d in s1}
        ans2 = {tuple(d.items()) for d in s2}
        union = ans1.union(ans2)
        intersect = ans1.intersection(ans2)
        union = [{
            "idx": item[0][1],
            "idy": item[1][1],
            "sm_score": item[2][1],
        } for item in union]
        intersect = [{
            "idx": item[0][1],
            "idy": item[1][1],
            "sm_score": item[2][1],
        } for item in intersect]
        return union, intersect

    def max_weight_matching(self, edges: list[dict]) -> list[dict]:
        # Extract unique node IDs
        node_ids = set()
        for edge in edges:
            node_ids.add(edge["idx"])
            node_ids.add(edge["idy"])
        node_ids = list(node_ids)
        node_ids.sort()
        # Create an adjacency matrix with edge weights
        num_nodes = len(node_ids)
        adjacency_matrix = np.zeros((num_nodes, num_nodes))
        for edge in edges:
            node1_index = node_ids.index(edge["idx"])
            node2_index = node_ids.index(edge["idy"])
            weight = edge["sm_score"]
            adjacency_matrix[node1_index, node2_index] = weight
        # Apply the Hungarian Algorithm
        row_ind, col_ind = linear_sum_assignment(-adjacency_matrix)
        # Display the maximum-weight matching
        matching = [(node_ids[row], node_ids[col]) for row, col in zip(row_ind, col_ind)]
        # Create the ans edges
        ans_edges = []
        for edge in edges:
            for match in matching:
                if edge["idx"] == match[0] and edge["idy"] == match[1]:
                    ans_edges.append(edge)
                    break
        return ans_edges

class JaccardMeasurement(Similarity_Measurement):
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
    measureFunc = JaccardMeasurement(0.5)
    assert measureFunc(str_x, str_y) == True

    # str_x = ["a", "b", "c"]
    # str_y = ["a", "d"]
    # assert measureFunc(str_x, str_y) == False

    # str_x = ["a", "b", "b", "c"]
    # str_y = ["a", "d"]
    # assert measureFunc(str_x, str_y) == False
