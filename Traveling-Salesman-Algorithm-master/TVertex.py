import random as rand
import copy
from collections.abc import Sequence
import math
import pygame

# VERTEX CLASS 
class Vertex:
    x      = float("nan")
    y      = float("nan")

    radius = 1
    alpha  = 150

    label = "Vertex"

    textFont    = pygame.font.SysFont("cascadiacoderegular", 20)
    textColor   = (0, 0, 0)


    def __init__(self,_x  = float(0), _y  = float(0),lb : str = "Vertex", _alpha : float = 150.0, _radius  : float = 1.0):
        self.x = _x
        self.y = _y
        self.alpha = _alpha
        self.radius = _radius
        self.label = lb
    
    def __str__(self):
        return self.Label+"(" + str(self.x)+" ; "+str(self.y)+") "

    # def __repr__(self):
    #     return str(self)

    def __eq__(self, o):
        if (not(o is Vertex)):
            return False
        return self.x == o.x and self.y == o.y and self.label == o.label


    def Draw(self, manager, showIndex=False, highlight=False, point_index=0):
        surface = pygame.Surface((self.radius *2, self.radius*2), pygame.SRCALPHA, 32)

        if highlight:
            r, g, b = manager.White
            pygame.draw.circle(surface, (r, g, b, 255), (self.radius, self.radius), self.radius)
            pygame.draw.circle(surface, (r, g, b, 255), (self.radius, self.radius), self.radius, 1)


        manager.screen.blit(surface, (int(self.x-self.radius), int(self.y-self.radius)))

        if showIndex:
            textSurface = self.textFont.render(str(point_index), True, self.textColor)
            textRectangle = textSurface.get_rect(center=(self.x, self.y))
            manager.screen.blit(textSurface, textRectangle)

    def GetTuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


