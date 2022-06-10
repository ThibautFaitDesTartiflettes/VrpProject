import random as rand
import copy
from collections.abc import Sequence
import math

# VERTEX CLASS 
class Vertex:
    X = 0
    Y = 0
    Label = "Vertex"

    def __init__(self, lb : str = "Vertex",_x : float = float("nan"), _y : float = float("nan")):
        if (math.isnan(_x)):
            _x = rand.randint(0, 100)
        if ( math.isnan(_y)):
            _y = rand.randint(0,100)

        self.X = _x
        self.Y = _y
        self.Label = lb
    
    def __str__(self):
        return self.Label+"(" + str(self.x)+" ; "+str(self.y)+") "

    def __repr__(self):
        return str(self)

    def __eq__(self, o):
        if (not(o is Vertex)):
            return False
        return self.X == o.X and self.Y == o.Y and self.Label == o.Label


