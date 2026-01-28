class Distance:
    def __init__(self):
        return self

    DOT = "Dot"
    COSINE = "Cosine"
    L2 = "L2"


class VectorConfig:
    def __init__(self, size=10, distance=""):
        self.dimension = size
        self.distance = distance
