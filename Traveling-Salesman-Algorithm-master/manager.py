import pygame
import random
from random import randint, sample
from point import Point
from utils import *
from genetic import Genetic
from antColony import *
from ant import *

offset          = 100
width, height   = 1920, 1080
populationSize  = 300
n = 15
colony_size = 10
iterations = 250
pygame.font.init()

class Manager(object):
    size            = (width, height)
    fps             = 60
    fpsOpti         = 60
    screen          = pygame.display.set_mode(size)
    clock           = pygame.time.Clock()
    scaler          = 1
    max_radius      = 15
    Black           = (25, 29, 31)
    White           = (200, 186, 168)
    Yellow          = (252, 192, 0)
    Gray            = (100, 107, 115)
    Highlight       = (255, 255, 0)
    LineThickness   = 4
    showIndex       = True
    n_points        = n
    timePassed      = 0
    timeMax         = 60
    # algorithms        = ["Brute Force", "Lexicographic Order", "Genetic Algorithm", "Ant Colony ACS", "Ant Colony Elitist", "Ant Colony Max-Min"]
    algorithms        = ["Brute Force",  "Genetic Algorithm", "Ant Colony"]

    genetic         = Genetic([sample(list(range(n)), n) for i in range(populationSize)], populationSize)

    PossibleCombinations = FactorialOpti(n_points)
    # print("possible combinations : {}".format(Factorial(n_points)))

    Order           = [i for i in range(n_points)]
    counter         = 0

    def __init__(self, Points = [Point(randint(offset, width-offset), randint(offset, height-offset)) for i in range(n_points)]):
        self.Points          = Points
        self.recordDistance  = SumDistance(self.Points)
        self.OptimalRoutes   = self.Points.copy()
        self.currentList     = self.Points.copy()

        # --- Ant Colony ---
        self.antColony = AntColony(size=colony_size, max_iterations = iterations,
                         nodes=self.Points.copy(), alpha=1, beta=3, rho=0.1, pheromone=1, phe_deposit_weight=1)

    def ResetGenetic(self):
        self.genetic = Genetic([sample(list(range(n)), n) for i in range(populationSize)], populationSize)

    def ResetAntColony(self):
        self.recordDistance  = SumDistance(self.Points)
        edges = self.antColony.edges
        self.antColony = AntColony( size=colony_size, max_iterations = iterations,
                         nodes=self.Points.copy(), alpha=1, beta=3, rho=0.1, pheromone=1, phe_deposit_weight=1,edges=edges)
    
    def SetFps(self):
        if (n > 100):
            return self.clock.tick(self.fps)/1000.0
        else:
            return self.clock.tick(self.fpsOpti)/1000.0

    def UpdateCaption(self):
        frameRate = int(self.clock.get_fps())
        pygame.display.set_caption("Traveling Salesman Problem - Fps : {}".format(frameRate))

    def Counter(self):
        self.counter += 1
        if self.counter > self.PossibleCombinations:
            self.counter = self.PossibleCombinations

    def BruteForce(self):
        if self.counter != self.PossibleCombinations:
            i1 = randint(0, self.n_points-1)
            i2 = randint(0, self.n_points-1)
            self.Points[i1], self.Points[i2] = self.Points[i2], self.Points[i1]

        # self.Counter()

        dist = SumDistance(self.Points)
        if dist < self.recordDistance:
            self.recordDistance  = dist
            self.OptimalRoutes   = self.Points.copy()
            #print("Shortest distance : {}" .format(self.recordDistance))

        self.DrawLines()

    def GeneticAlgorithm(self):

        self.genetic.CalculateFitness(self.Points)
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
        if (n <= 100):
            self.antColony.Draw(self)
        self.recordDistance = self.antColony.best_distance

    def RandomPoints(self):
        self.Points = [Point(randint(offset/2, width-5*offset), randint(offset, height-offset)) for i in range(self.n_points)]
        self.ResetAntColony()
        self.recordDistance  = SumDistance(self.Points)
        self.OptimalRoutes   = self.Points.copy()
        self.currentList     = self.Points.copy()

    def Percentage(self):
        percent = (self.counter/iterations) * 100
        percentTime = (self.timePassed/self.timeMax) * 100
        if (n<=100):
            textFont    = pygame.font.SysFont("cascadiacoderegular", 20)
        else:
            textFont    = pygame.font.SysFont("cascadiacoderegular", 50)

        textSurface = textFont.render("iteration : "+str(round(percent, 2))+"%", False, self.White)
        textSurface2 = textFont.render("time : "+str(round(percentTime, 2))+"%", False, self.White)

        if (n<=100):
            self.screen.blit(textSurface, (width//2, 25))
            self.screen.blit(textSurface2, (width//2, 50))
        else:
            self.screen.blit(textSurface, (width//2-200, 30))
            self.screen.blit(textSurface2, (width//2-200, 70))

    def ShowText(self, selectedIndex, started = True, time = 0, iterTime = 0):
        textColor   = (255, 255, 255)
        textFont    = pygame.font.SysFont("cascadiacoderegular", 20)
        textFont2    = pygame.font.SysFont("cascadiacoderegular", 40)

        textSurface1 = textFont.render("Best distance : " + str(round(self.recordDistance,2)), False, textColor)
        textSurface2 = textFont.render(self.algorithms[selectedIndex], False, textColor)
        textSurface_ale =  textFont.render('time = '+str(round(self.timePassed,2))+' s', False, textColor)
        textSurface_count =  textFont.render('iteration = '+str(self.counter), False, textColor)
        textSurface_time =  textFont.render('time : '+GetTimeStr(time), False, textColor)
        textSurface_iterTime =  textFont.render('iteration time : '+str(round(iterTime,3)), False, textColor)
    
        self.screen.blit(textSurface1, (20, 50))
        self.screen.blit(textSurface2, (20, 25))
        self.screen.blit(textSurface_ale, (20, 75))
        self.screen.blit(textSurface_count, (20,100))
        self.screen.blit(textSurface_iterTime, (20, 125))
        self.screen.blit(textSurface_time, (width-270,50))

        if (n>100):
            textSurface_result = textFont2.render(" --> ".join([str(i) for i in self.OptimalRoutes]), False, textColor)
            self.screen.blit(textSurface_result,( 0,height//2 -20))

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
        for point in self.Points:
            point.radius = self.scaler
            point.Draw(self)

    def DrawLines(self, drawCurrent=False):
        if drawCurrent == True:
            for i, point in enumerate(self.currentList):
                _i = (i+1)%len(self.currentList)
                pygame.draw.line(self.screen, self.Gray, (point.x, point.y), (self.currentList[_i].x, self.currentList[_i].y), 1)
        else:
            for i, point in enumerate(self.Points):
                _i = (i+1)%len(self.Points)
                pygame.draw.line(self.screen, self.Gray, (point.x, point.y), (self.Points[_i].x, self.Points[_i].y), 1)

    def Background(self):
        self.screen.fill(self.Black)

    def ResetGraph(self):
        temp = self.Points.copy()
        #self.__init__(temp)
        self.OptimalRoutes = self.Points.copy()
        self.recordDistance = SumDistance(self.Points)
        self.ResetAntColony()
        self.ResetGenetic()
        self.timePassed = 0
        self.counter = 0