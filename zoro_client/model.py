from enum import Enum


class Distance(str, Enum):
    DOT = "Dot"
    COSINE = "Cosine"
    L2 = "L2"


class VectorConfig:
    def __init__(self, size=10, distance=""):
        self.dimension = size
        self.distance = distance
