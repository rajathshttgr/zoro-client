from enum import Enum


class Distance(str, Enum):
    DOT = "dot"
    COSINE = "cosine"
    L2 = "l2"


class VectorConfig:
    def __init__(self, size=1, distance=""):
        self.dimension = size
        self.distance = distance
