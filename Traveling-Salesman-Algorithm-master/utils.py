from math import sqrt
from random import randint, uniform
from TGraph import *
from TEdge import *

def Distance(a, b):
    return sqrt( (b.x-a.x)*(b.x-a.x) + (b.y-a.y)*(b.y-a.y) )

def SumDistance(pointOrder,graph):
    s = 0
    for i in range(len(pointOrder)):
        # dist = Distance(points[i], points[(i+1) % len(points)])
        dist = graph.__getitem__(pointOrder[i], pointOrder[(i+1)%len(pointOrder)]).weight
        if (dist == -1):
            return -1
        s += dist
    return s

def PickSelection(myList, probabilities):
    i = 0
    r = uniform(0, 1)
    while r > 0:
        r -= probabilities[i]
        i += 1
    i -= 1
    return myList[i]

def translateValue(value, min1, max1, min2, max2):
    return min2 + (max2 - min2)* ((value-min1)/(max1-min1))

def Factorial(n):
    if n == 1:
        return 1
    else:
        return n * Factorial(n - 1)
