import random as rand
from math import *
import copy
from collections.abc import Sequence
import math
import sys
from TEdge import *
from TVertex import *

class IdxVertex(Vertex):
    idx : int = -1

    def __init__(self,_idx : int, pt : Vertex):
        Vertex.__init__(self,pt.x,pt.y,pt.label,pt.alpha,pt.radius)
        self.idx = _idx

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y and self.label == o.label



# GRAPH CLASS 
class Graph(Sequence):
    Vertex = []
    Edges = []


    def __init__(self,L:int = 0):
        self.L = L
        super().__init__()

    def addVertex(self,pt : Vertex):
        self.Vertex.append(IdxVertex(len(self.Vertex),pt))
        self.Edges.append( [Edge() for i in range(len(self.Edges))])
        for i in range(len(self.Edges)):
            self.Edges[i].append(Edge())

    def removeVertex(self ,pt : Vertex):
        for idx_pt in range(len(self.Vertex)) :
            if (self.Vertex[idx_pt] == pt):
                self.removeVertex(idx_pt)
                return

    def removeVertex(selft, idx : int):
        self.Vertex.pop(idx)
        self.Edges.pop(idx)
        for i in range(len(self.Edges)):
            self.Edges[i].pop(idx)


    def __getitem__(self, i,j):
        return self.Edges[i][j]

    def __len__(self):
        count = 0
        for i in range(len(self.Vertex)):
            count+=len(self.Vertex)

    def clearVertex(self):
        self.Vertex = []
        self.Edges = []

    def addEdges(self,pt1 : Vertex , pt2 : Vertex, weight : float = 1):
        if (not ( pt1 in self.Edges[0] and pt2 in self.Edges[0])):
            return   
        idx1 = self.getIndex(pt1)
        idx2 = self.getIndex(pt2)
        self.setEdges(idx1, idx2, weight)

    def setEdges(self,idx1 : int , idx2 : int, weight : float):
        self.Edges[idx1][idx2].weight = weight
        self.Edges[idx2][idx1].weight = weight
    
    def getIndex(self,pt : Vertex):
        for i in range(len(self.Vertex)):
            if (pt == self.Vertex[i]):
                return i
    
    def getDeg(self, pt : Vertex):
        idx = self.getIndex(pt)
        deg  = 0
        for i in range(len(self.Edges)):
            if (self.Edges[idx][i].weight==0):
                continue
            deg+=1
        return deg

    def setVertex(self, pts):
        self.Edges.clear()
        self.Vertex.clear()
        for pt in pts:
            self.addVertex(pt)

    def getPtIndex(self, pt):
        for iv in self.Vertex:
            if iv == pt:
                return iv.idx

