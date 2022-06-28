import matplotlib.pyplot as plt
import random as rand
from matplotlib import style
from matplotlib.widgets import Button
from math import *
import copy
from collections.abc import Sequence
import math
import sys
from TVertex import Vertex
from TGraph import Graph



# program class
class Program:

    g = Graph()
    alphabet = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
    fig, ax = plt.subplots()

    def Main(self):
        #init the graph
        style.use('fivethirtyeight')
        plt.subplots_adjust(bottom=0.2)

        axprev = plt.axes([0.9, 0.00, 0.1, 0.05])
        bprev = Button(axprev, 'ReGen')
        bprev.color = 'b'
        bprev.hovercolor = 'g'
        bprev.on_clicked(self.prev)

        self.RefreshAll()
        plt.show()

    # call on button clique
    def prev(self, event):
        self.RefreshAll()

    #draw the graph g in the plot
    def DrawGraph(self):
        self.ax.cla()
        self.ax.axis('off')

        #draw the line (= edges)
        for i in range(0,len(self.g.Vertex)):
            for j in range(i,len(self.g.Vertex)):
                if (self.g.Edges[i][j].weight==0):
                    continue
                pt1 = self.g.Vertex[i]
                pt2 = self.g.Vertex[j]
                #self.ax.plot(pt1.X,pt1.Y,pt2.X,pt2.Y,color='black')
                self.ax.arrow(pt1.X,pt1.Y,pt2.X -pt1.X,pt2.Y-pt1.Y,width=0.1,color='black',head_length=0.0,head_width=0.0)
                xText = float(pt1.X + (pt2.X - pt1.X)/2)
                yText =float(pt1.Y +(pt2.Y - pt1.Y)/2)
                self.ax.text(xText, yText, str(self.g.Edges[i][j].weight),fontsize=10)

        # draw the point
        for i in range(len(self.g.Vertex)):
            pt = self.g.Vertex[i]
            self.ax.scatter(pt.X, pt.Y, marker='x', color='red',linewidths=1)
            self.ax.text(pt.X, pt.Y+1, pt.Label, fontsize=10, weight='bold')
        plt.draw()


    # regen the graph
    def RefreshAll(self):

        # generation of vertex
        count = rand.randint(4,8)
        self.g.clearVertex()
        for i in range(count):
            self.g.addVertex(Vertex( self.alphabet[i]))            

        # generation of edges
        for i in range(count):
            for j in range(i,count):
                if ((self.g.getDeg(self.g.Vertex[i]) >= 2 and self.g.getDeg(self.g.Vertex[j]) >= 2) or i == j):
                #if (rand.randint(0, 100)%2==0):
                    continue
                self.g.setEdges(i, j, rand.randint(1, 10))
        
        self.DrawGraph()
    
pgrm = Program()
pgrm.Main()
