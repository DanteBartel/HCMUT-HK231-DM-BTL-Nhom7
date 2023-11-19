from similarity_measurement import Similarity_Measurement, EditDistanceMeasurement, GeneralizedJaccard

class BoundFiltering(object):
    sm: Similarity_Measurement

    def __init__(self, sm: Similarity_Measurement) -> None:
        self.sm = sm
        return

    def __call__(self) -> int:
        """
        + Calculating upper bound and lower bound.
        + Return the answer or skip based on bounds.
        + 0 means ignore this pair
        + 1 means this pair is an answer
        + 2 means need to calculate Similarity Measurement
        """
        ub, lb = self.sm.bound()
        if ub < self.sm.threshold: return 0
        elif lb >= self.sm.threshold: return 1
        else: return 2