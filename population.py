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
        self.best_objective = 0

    def init_population(self):
        for i in range(self.population_size):
            route = [np.random.randint(self.distance_matrix.shape[0])]

            for j in range(self.distance_matrix.shape[0] - 1):
                infinity_edges = set()
                for k in range(self.distance_matrix.shape[0]-1):
                    if self.distance_matrix[route[-1], k] == 'Inf':
                        infinity_edges.add(k)
                choices = set(range(self.distance_matrix.shape[0])) - set(route) - infinity_edges
                route.append(random.choice(list(choices)))

            self.population[i] = Individual(route)

        return self.population

    def k_tournament(self, k):
        selected = random.sample(list(self.population), k)
        values = [individual.cost_function(self.distance_matrix) for individual in selected]
        return selected[np.argmin(values)]

