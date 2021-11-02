"""
Class which holds the population

"""

import numpy as np
from individual import Individual
import random

class Population:

    def __init__(self, population_size, distance_matrix):
        self.population_size = population_size
        self.distance_matrix = distance_matrix
        self.population = np.empty(self.population_size, dtype=Individual)
        self.mean_objective = 0

    def init_population(self):
        for i in range(self.population_size):
            route = self.random_depth_first_search()
            self.population[i] = Individual(route)

    def random_depth_first_search(self):
        # Create possible goal nodes for each node, eliminate 'inf' and zero values
        possible_nodes = []
        for i in range(self.distance_matrix.shape[0]):
            possible_nodes.append([])
            for j in range(self.distance_matrix.shape[0]):
                if not (np.isinf(self.distance_matrix[i, j]) or self.distance_matrix[i, j] == 0):
                    possible_nodes[i].append(j)

        # shuffle each set of goal nodes
        for i in range(len(possible_nodes)):
            random.shuffle(possible_nodes[i])

        # choose random start point and remove from edge table
        route = [np.random.randint(self.distance_matrix.shape[0])]
        for i in range(len(possible_nodes)):
            if route[-1] in possible_nodes[i]:
                possible_nodes[i].remove(route[-1])

        # discovered
        discovered = [[]] * self.distance_matrix.shape[0]

        # main loop
        while len(route) < self.distance_matrix.shape[0]:
            if len(possible_nodes[route[-1]]) > 0:
                # add first element of nodes connected vertices
                route.append(possible_nodes[route[-1]][0])
                for i in range(len(possible_nodes)):
                    if route[-1] in possible_nodes[i]:
                        possible_nodes[i].remove(route[-1])
                        discovered[i].append(route[-1])
            else:
                # backtrack
                # remove from route
                last = route[-1]
                route = route[0:len(route) - 1]
                for i in range(self.distance_matrix.shape[0]):
                    if last in discovered[i] and i not in route:
                        possible_nodes[i].insert(0, last)
        return route

    def k_tournament_selection(self, k):
        selected = random.sample(list(self.population), k)
        values = [individual.cost_function(self.distance_matrix) for individual in selected]
        return selected[np.argmin(values)]

    def k_tournament_elimination(self, k):
        selected = random.sample(list(self.population), k)
        values = [individual.cost_function(self.distance_matrix) for individual in selected]
        return selected[np.argmax(values)]

    def calculate_stats(self):
        costs = [i.cost_function(self.distance_matrix) for i in self.population]
        self.best_solution = self.population[costs.index(min(costs))]
        self.mean_objective = np.mean(costs)

    def breed(self, offspring_size, k, mutation_prob):
        offspring = []
        for i in range(offspring_size):
            parent1 = self.k_tournament_selection(k)
            parent2 = self.k_tournament_selection(k)
            offspring.append(Individual(parent1.edge_crossover(parent2)))
            offspring[-1].random_mutation(mutation_prob)
        self.population = np.concatenate((self.population, np.array(offspring)))
        self.population_size = len(self.population)

    def elimination(self, new_size, k):
        for i in range(self.population_size-new_size):
            self.population = self.population[self.population != self.k_tournament_elimination(k)]
        self.population_size = new_size
