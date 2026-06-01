import numpy as np


class strategy:
    def __init__(self, strattype="Responsive"):
        self.strattype = strattype
        self.state = False
        self.highquality = True
        self.freqACT = 1
        self.freqPAS = 1
        self.freq = 1
        self.memorycap = 10
        self.memory = 0
        self.costs = np.array([1, 2])
        self.currentcost = 1
