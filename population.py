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
            route = [np.random.randint(self.distance_matrix.shape[0])]

            for j in range(self.distance_matrix.shape[0] - 1):
                infinity_edges = set()
                for k in range(self.distance_matrix.shape[0]-1):
                    if np.isinf(self.distance_matrix[route[-1], k]):
                        infinity_edges.add(k)
                choices = set(range(self.distance_matrix.shape[0])) - set(route) - infinity_edges
                if len(choices) == 0:
                    a = [i for i in range(self.distance_matrix.shape[0]) if i not in route]
                    random.shuffle(a)
                    route = np.concatenate((route, a))
                    break
                route.append(random.choice(list(choices)))

            self.population[i] = Individual(route)
            # self.population[i] = Individual(np.random.permutation(self.distance_matrix.shape[0]))

        return self.population

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
