import pygame
import math
import random

class Edge:



    def __init__(self, a, b, heuristic, pheromone, coef1, coef2 , coef3, coef4):
        self.a = a
        self.b = b
        self.heuristic = heuristic
        self.pheromone = pheromone
        self.coef1 = coef1
        self.coef2 = coef2
        self.coef3 = coef3
        self.coef4 = coef4

    def CalcDist(self , time):
        v = 0
        v+=((self.coef1 * math.cos(time*2 *math.pi))/(6))
        v+=((self.coef2 * math.cos(time*3 * math.pi)+1)/(6))
        v+=((self.coef3 * math.cos(time*4 * math.pi)+1)/(6))
        v+=((self.coef4 * math.cos(time*5 * math.pi)+1)/(6))
        return v


        

class Ant:
    def __init__(self, edges, alpha, beta, n_nodes,time):
        """
        alpha -> parameter used to control the importance of the pheromone trail
        beta  -> parameter used to control the heuristic information during selection
        """
        self.edges = edges
        self.tour = None
        self.alpha = alpha
        self.beta = beta
        self.n_nodes = n_nodes
        self.distance = 0.0
        self.time = time

    def NodeSelection(self):
        """
        Constructing solution
        an ant will often follow the strongest
        pheromone trail when constructing a solution.

        state -> is a point on a graph or a City

        Here, an ant would be selecting the next city depending on the distance
        to the next city, and the amount of pheromone on the path between
        the two cities.
        """
        roulette_wheel = 0
        states = [node for node in range(self.n_nodes) if node not in self.tour]
        heuristic_value = 0
        for new_state in states:
            # heuristic_value += self.edges[self.tour[-1]][new_state].heuristic
            heuristic_value += self.edges[self.tour[-1]][new_state].CalcDist(self.time)
        for new_state in states:
            A = math.pow(self.edges[self.tour[-1]][new_state].pheromone, self.alpha)
            B = math.pow((heuristic_value/self.edges[self.tour[-1]][new_state].CalcDist(self.time)), self.beta)
            # B = math.pow((heuristic_value/self.edges[self.tour[-1]][new_state].heuristic), self.beta)
            roulette_wheel += A * B
        random_value = random.uniform(0, roulette_wheel)
        wheel_position = 0
        for new_state in states:
            A = math.pow(self.edges[self.tour[-1]][new_state].pheromone, self.alpha)
            # B = math.pow((heuristic_value/self.edges[self.tour[-1]][new_state].heuristic), self.beta)
            B = math.pow((heuristic_value/self.edges[self.tour[-1]][new_state].CalcDist(self.time)), self.beta)
            wheel_position += A * B
            if wheel_position >= random_value:
                return new_state

    def UpdateTour(self):
        self.tour = [random.randint(0, self.n_nodes - 1)]
        while len(self.tour) < self.n_nodes:
            n = self.NodeSelection()
            self.tour.append(n)
            self.time += (self.edges[self.tour[len(self.tour)-1]][self.tour[len(self.tour)-2]]).CalcDist(self.time%1)
            self.time = self.time
        return self.tour

    def CalculateDistance(self):
        self.distance = 0
        for i in range(self.n_nodes):
            self.distance += self.edges[self.tour[i]][self.tour[(i+1)%self.n_nodes]].heuristic
        return self.distance
