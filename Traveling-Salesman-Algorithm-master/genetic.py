from utils import *
from random import randint
from TGraph import *
from TVertex import *

class Genetic:
    # def __init__(self, population=[], populationSize=0):
    def __init__(self, graph : Graph):
        # self.population = population
        self.graph = graph
        # self.size = populationSize
        self.size = len(self.graph.Vertex)
        self.fitness = [0 for i in range(self.size)]
        self.record = float("inf")
        self.currentDist = float("inf")
        self.current = None
        self.fitest = []
        self.fitestIndex = 0
        self.mutation_rate = 0.01

    def CalculateFitness(self, vertexes):
        for i in range(self.size):
            nodes = []
            # for j in self.population[i]:
            # for j in self.graph.Edges[i]:
                # nodes.append(vertexes[j])
            nodes.append(vertexes.Vertex[i])
            #print(nodes)
            order = [i for i in range(len(nodes))]
            # dist = SumDistance(nodes)
            dist = SumDistance(order, self.graph)

            if dist < self.currentDist and dist >0 :
                # self.current = self.population[i]
                self.current = self.graph.Vertex[i]

            if dist < self.record and dist > 0:
                self.record = dist
                self.fitest = self.graph.Vertex[i]
                # self.fitest = self.population[i]
                self.fitestIndex = i
                #print(f"Shortest distance: {dist}")
            
            if (dist <= 0):
                self.fitness[i] = float("inf")
            else :
                self.fitness[i] = 1/ (dist+1)

        self.NormalizeFitnesss()

    def NormalizeFitnesss(self):
        s = 0
        for i in range(self.size):
            s += self.fitness[i]
        for i in range(self.size):
            self.fitness[i] = self.fitness[i]/s

    def Mutate(self, genes):
        # for i in range(len(self.population[0])):
        for i in range(len(self.graph.Edges[0])):
            if (randint(0, 100)/100) < self.mutation_rate:
                a = randint(0, len(genes)-1)
                b = randint(0, len(genes)-1)
                genes[a], genes[b] = genes[b], genes[a]

    def CrossOver(self, genes1, genes2):
        start = randint(0, len(genes1)-1)
        end   = randint(start-1, len(genes2)-1)
        try:
            end = randint(start+1, len(genes2)-1)
        except:
            pass
        new_genes = genes1[start:end]
        for i in range(len(genes2)):
            p = genes2[i]
            if p not in new_genes:
                new_genes.append(p)
        return new_genes

    def NaturalSelection(self):
        nextPopulation = []
        for i in range(self.size):
            generation1 = PickSelection(self.graph.Edges, self.fitness)
            # generation1 = PickSelection(self.population, self.fitness)
            generation2 = PickSelection(self.graph.Edges, self.fitness)
            # generation2 = PickSelection(self.population, self.fitness)
            genes = self.CrossOver(generation1, generation2)
            self.Mutate(genes)
            nextPopulation.append(genes)
        # self.population = nextPopulation
        self.graph.setVertex( nextPopulation)
