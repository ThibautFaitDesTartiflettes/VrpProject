import pygame
from ant import *
from utils import translateValue
pygame.font.init()
textColor   = (0, 0, 0)
# textFont    = pg.font.Font("freesansbold.ttf", size)
textFont    = pygame.font.SysFont("cascadiacoderegular", 20)

class AntColony(object):
    def __init__(self, size=5, elitist_weight=1.0, minFactor=0.001, alpha=1.0, beta=3.0,
                 rho=0.1, phe_deposit_weight=1.0, pheromone=1.0, max_iterations=100, nodes=None, labels=None):
        self.size = size
        self.alpha = alpha
        self.rho = rho
        self.phe_deposit_weight = phe_deposit_weight
        self.max_iterations = max_iterations
        self.n_nodes = len(nodes)
        self.nodes = nodes
        self.edges = [[None for j in range(self.n_nodes)] for i in range(self.n_nodes)]
        for x in range(self.n_nodes):
            for y in range(self.n_nodes):
                heuristic = math.sqrt(
                    math.pow(self.nodes[x].x-self.nodes[y].x, 2) +
                    math.pow(self.nodes[x].y-self.nodes[y].y, 2)
                )
                self.edges[x][y] = self.edges[y][x] = Edge(x, y, heuristic, pheromone)
        self.ants = [Ant(self.edges, alpha, beta, self.n_nodes) for i in range(self.size)]

        # global Best route
        self.best_tour = []
        self.best_distance = float("inf")

        self.local_best_route = []
        self.local_best_distance = float("inf")

    def AddPheromone(self, tour, distance, heuristic=1):
        pheromone_to_add = self.phe_deposit_weight / distance
        for i in range(self.n_nodes):
            self.edges[tour[i]][tour[(i + 1) % self.n_nodes]].pheromone += heuristic

    def Simulate(self):
        # for step in range(self.max_iterations):
        for ant in self.ants:
            self.AddPheromone(ant.UpdateTour(), ant.CalculateDistance())
            if ant.distance < self.best_distance:
                self.best_tour = ant.tour
                self.best_distance = ant.distance

        for x in range(self.n_nodes):
            for y in range(x + 1, self.n_nodes):
                self.edges[x][y].pheromone *= (1 - self.rho)

    def Draw(self, manager):
        manager.OptimalRoutes = [manager.Points[i] for i in self.best_tour]

        # Draw Pheromones
        for ant in self.ants:
            for edge in ant.edges:
                for e in edge:
                    r = g = b = int(min((e.pheromone)*2, 255))
                    thickness = int(translateValue(e.pheromone, 0, 255, 1, 8))
                    pygame.draw.line(manager.screen, (r, g, 0), self.nodes[e.a].GetTuple(), self.nodes[e.b].GetTuple(), thickness)


        for node in self.nodes:
            pygame.draw.circle(manager.screen, manager.White, node.GetTuple(), manager.scaler)

        for i in self.best_tour:
            textSurface = textFont.render(str(i), True, textColor)
            textRectangle = textSurface.get_rect(center=(self.nodes[self.best_tour[i]].x, self.nodes[self.best_tour[i]].y))
            manager.screen.blit(textSurface, textRectangle)
