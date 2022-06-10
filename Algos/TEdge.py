
from math import *
import copy
import math
from TVertex import Vertex

class Edge:
    weight = 0
    pt1 : Vertex = None
    pt2 : Vertex = None

    def __init__(self,_weight : float = 0):
        self.weight = _weight
