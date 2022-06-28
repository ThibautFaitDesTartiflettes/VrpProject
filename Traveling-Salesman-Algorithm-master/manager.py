import pygame
import random
from random import randint, sample
from point import Point
from utils import *
from genetic import Genetic
from antColony import *
from ant import *
from TGraph import *
from TEdge import *
from TVertex import *

offset          = 100
width, height   = 1920, 1080
populationSize  = 300
n = 7
colony_size = 10
iterations = 2500
timeMax= 180
pygame.font.init()

class Manager(object):
    size= (width, height)
    fps= 60
    screen= pygame.display.set_mode(size)
    clock= pygame.time.Clock()
    scaler= 1
    max_radius= 15
    Black= (25, 29, 31)
    White= (200, 186, 168)
    Yellow= (252, 192, 0)
    Gray= (100, 107, 115)
    Highlight= (255, 255, 0)
    LineThickness= 4
    showIndex= True
    n_points= n
    timePassed= 0
    algorithms = ["Brute Force",  "Genetic Algorithm", "Ant Colony"]
    

    #modif ALE
    graphAdj = Graph()


    PossibleCombinations = Factorial(n_points)

    # Order = [i for i in range(n_points)]
    counter = 0

    def __init__(self, Points = [Vertex(randint(offset, width-offset), randint(offset, height-offset)) for i in range(n_points)]):
        #self.Points          = Points
        self.graphAdj.setVertex(Points)
        self.Order = []
        self.CalcDefaultOrder()
        self.recordDistance  = SumDistance(self.Order,self.graphAdj)
        # self.OptimalRoutes   = self.Points.copy()
        self.OptimalRoutes   = self.graphAdj.Vertex.copy()
        # self.currentList     = self.Points.copy()
        self.currentList     = self.graphAdj.Vertex.copy()
        self.n_points = len(self.graphAdj.Vertex)

        # --- Ant Colony ---
        # self.antColony = AntColony(size=colony_size, max_iterations = iterations,
        #                  nodes=self.Points.copy(), alpha=1, beta=3, rho=0.1, pheromone=1, phe_deposit_weight=1)
        self.antColony = AntColony(size=colony_size, max_iterations = iterations,
                         graph=self.graphAdj, alpha=1, beta=3, rho=0.1, pheromone=1, phe_deposit_weight=1)
        
        # self.genetic= Genetic([sample(list(range(n)), n) for i in range(populationSize)], populationSize)
        self.genetic= Genetic(self.graphAdj)
        


    def ResetGenetic(self):
        self.genetic = Genetic(self.graphAdj)
        # self.genetic = Genetic([sample(list(range(n)), n) for i in range(populationSize)], populationSize)

    def ResetAntColony(self):
        # self.recordDistance  = SumDistance(self.Points)
        self.recordDistance  = SumDistance(self.Order,self.graphAdj)
        self.antColony = AntColony( size=colony_size, max_iterations = iterations,
                         graph=self.graphAdj, alpha=1, beta=3, rho=0.1, pheromone=1, phe_deposit_weight=1)
                        #  nodes=self.Points.copy(), alpha=1, beta=3, rho=0.1, pheromone=1, phe_deposit_weight=1)
    
    def SetFps(self):
        return self.clock.tick(self.fps)/1000.0

    def UpdateCaption(self):
        frameRate = int(self.clock.get_fps())
        pygame.display.set_caption("Traveling Salesman Problem - Fps : {}".format(frameRate))

    def Counter(self):
        self.counter += 1
        if self.counter > self.PossibleCombinations:
            self.counter = self.PossibleCombinations

    def BruteForce(self):
        # if self.counter != self.PossibleCombinations:
        
        i1 = randint(0, self.n_points-1)
        list = [j for j in range(self.n_points) if self.graphAdj.__getitem__(i1, j).weight != -1]
        i2 = list[randint(0, len(list)-1)]

        temp = self.Order[i1]
        self.Order[i1] = self.Order[i2]
        self.Order[i2] = temp

        # self.Points[i1], self.Points[i2] = self.Points[i2], self.Points[i1]

        # self.Counter()

        # dist = SumDistance(self.Points)

        dist = SumDistance(self.Order,self.graphAdj)
        print("path : "+" --> ".join([str(i) for i in self.Order]) + "  ("+str(dist)+" )")
        if dist < self.recordDistance and dist > 0:
            self.recordDistance  = dist
            self.OptimalRoutes   =[self.graphAdj.Vertex[i] for i in self.Order]
            # self.OptimalRoutes   = self.Points.copy()
            #print("Shortest distance : {}" .format(self.recordDistance))

        self.DrawLines()

    def GeneticAlgorithm(self):

        # self.genetic.CalculateFitness(self.Points)
        self.genetic.CalculateFitness(self.graphAdj)
        self.genetic.NaturalSelection()

        for i in range(self.n_points):
            self.currentList[i] = self.Points[self.genetic.current[i]]

        if self.genetic.record < self.recordDistance:
            for i in range(self.n_points):
                self.OptimalRoutes[i] = self.Points[self.genetic.fitest[i]]
            self.recordDistance = self.genetic.record

        self.DrawLines(True)

    def AntColonyOptimization(self):
        self.antColony.Simulate()
        self.antColony.Draw(self)
        self.recordDistance = self.antColony.best_distance

    def RandomPoints(self):
        # self.Points = [Point(randint(offset/2, width-5*offset), randint(offset, height-offset)) for i in range(self.n_points)]
        self.graphAdj.clearVertex()
        for i in range(self.n_points):
            v = Vertex(randint(offset/2, width-5*offset),randint(offset, height-offset))
            self.graphAdj.addVertex(v)

        #generate edges
        for i in range(self.n_points):
            counter =0
            if (self.n_points-1-i-2 > 0):
                edges = randint(2, self.n_points-1-i)
            else:
                edges = randint(0, self.n_points -1- i)
            while (counter < edges):
                j = randint(i+1, self.n_points-1)
                if (self.graphAdj.Edges[i][j].weight != -1):
                    continue
                counter+=1
                self.graphAdj.setEdges(i, j, randint(1,100))
            
            #debug
            print("MATRIX ADJACENCE")
            for i in range(self.n_points):
                print(" | ".join( str(self.graphAdj.Edges[i][j].weight) for j in range(self.n_points) ))




        self.ResetAntColony()
        self.recordDistance  = SumDistance(self.Order,self.graphAdj)
        # self.OptimalRoutes   = self.Points.copy()
        self.OptimalRoutes   = [self.graphAdj.Vertex[i] for i in self.Order]
        # self.currentList     = self.Points.copy()
        self.currentList     = self.graphAdj.Vertex.copy()

    def Percentage(self):
        percent = (self.counter/iterations) * 100
        percentTime = (self.timePassed/timeMax) * 100
        textFont    = pygame.font.SysFont("cascadiacoderegular", 20)
        textSurface = textFont.render("iteration : "+str(round(percent, 2))+"%", False, self.White)
        textSurface2 = textFont.render("time : "+str(round(percentTime, 2))+"%", False, self.White)
        self.screen.blit(textSurface, (width//2, 25))
        self.screen.blit(textSurface2, (width//2, 50))

    def ShowText(self, selectedIndex, started = True):
        textColor   = (255, 255, 255)
        textFont    = pygame.font.SysFont("cascadiacoderegular", 20)
        textFont2    = pygame.font.SysFont("cascadiacoderegular", 40)

        textSurface1 = textFont.render("Best distance : " + str(round(self.recordDistance,2)), False, textColor)
        textSurface2 = textFont.render(self.algorithms[selectedIndex], False, textColor)
        textSurface_ale =  textFont.render('time = '+str(round(self.timePassed,2))+' s', False, textColor)
        textSurface_count =  textFont.render('iteration = '+str(self.counter), False, textColor)

        self.screen.blit(textSurface1, (20, 50))
        self.screen.blit(textSurface2, (20, 25))
        self.screen.blit(textSurface_ale, (20, 75))
        self.screen.blit(textSurface_count, (20,100))

    def DrawShortestPath(self):
        if len(self.OptimalRoutes) > 0:
            for n in range(self.n_points):
                _i = (n+1)%self.n_points
                pygame.draw.line(self.screen, self.Highlight,
                                (self.OptimalRoutes[n].x, self.OptimalRoutes[n].y),
                                (self.OptimalRoutes[_i].x, self.OptimalRoutes[_i].y),
                                self.LineThickness)
                self.OptimalRoutes[n].Draw(self, self.showIndex, True, n)

    def DrawPoints(self, selected_index = 0):
        # for point in self.Points:
        for point in self.graphAdj.Vertex:
            point.radius = self.scaler
            point.Draw(self)

    def DrawLines(self, drawCurrent=False):
        if drawCurrent == True:
            for i, point in enumerate(self.currentList):
                _i = (i+1)%len(self.currentList)
                pygame.draw.line(self.screen, self.Gray, (point.x, point.y), (self.currentList[_i].x, self.currentList[_i].y), 1)
        else:
            # for i, point in enumerate(self.Points):
            # for i, point in enumerate(self.graphAdj.Vertex):
            for i in range(len(self.Order)):
                idx1 = self.Order[i]
                idx2 = self.Order[(i+1)%len(self.Order)]
                _i = (i+1)%len(self.graphAdj.Vertex)
                # pygame.draw.line(self.screen, self.Gray, (point.x, point.y), (self.Points[_i].x, self.Points[_i].y), 1)
                # pygame.draw.line(self.screen, self.Gray, (point.x, point.y), (self.graphAdj.Vertex[_i].x, self.graphAdj.Vertex[_i].y), 1)
                pt1 = self.graphAdj.Vertex[idx1]
                pt2 = self.graphAdj.Vertex[idx2]
                pygame.draw.line(self.screen, self.Gray, (pt1.x,pt1.y), (pt2.x, pt2.y), 1)

    def Background(self):
        self.screen.fill(self.Black)

    def ResetGraph(self):
        # temp = self.Points.copy()
        temp = self.graphAdj.Vertex.copy()
        # self.__init__(temp)
        # self.OptimalRoutes = self.Points.copy()
        self.OptimalRoutes = self.graphAdj.Vertex.copy()
        # self.Order = [i for i in range(len(self.graphAdj.Vertex))]
        self.CalcDefaultOrder()
        # self.recordDistance = SumDistance(self.Points)
        self.recordDistance = SumDistance(self.Order, self.graphAdj)
        self.ResetAntColony()
        self.ResetGenetic()
        self.timePassed = 0
        self.counter = 0
    
    def CalcDefaultOrder(self):
        self.Order.clear()
        self.Order.append(0)
        for i in range(self.n_points):
            for j in range(self.n_points):
                if ((self.graphAdj.__getitem__(i, j).weight != -1) and not(j in self.Order)):
                    nextIdx = j
                    self.Order.append(nextIdx)
                    break
        if (len(self.Order) != self.n_points):
            self.OptimalRoutes = [Vertex() for i in range(self.n_points)]
        else:
            self.OptimalRoutes = [self.graphAdj.Vertex[i] for i in self.Order]

