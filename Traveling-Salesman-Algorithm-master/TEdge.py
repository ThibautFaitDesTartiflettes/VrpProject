
from math import *
import copy
import math
from TVertex import Vertex

class Edge:

    weight = -1

    def __init__(self,a = 0, b = 0, heuristic = 1, pheromone = 0, _weight  : float = -1):
        self.weight = _weight
        self.a = a
        self.b = b
        self.heuristic = heuristic
        self.pheromone = pheromone

    def __str__(self):
        return str(self.weight)

    def __repr__(self):
        return str(self)
