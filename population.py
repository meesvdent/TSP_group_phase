"""
Class which holds the population

"""

import numpy as np
from individual import Individual
import random
from multiprocessing import Pool
import copy

class Population:

    def __init__(self, population_size, distance_matrix):
        self.population_size = population_size
        self.distance_matrix = distance_matrix
        self.population = np.empty(self.population_size, dtype=Individual)
        self.mean_objective = 0
        self.__processes__= 8

    # def init_population(self):
    #     for i in range(self.population_size):
    #         route = [np.random.randint(self.distance_matrix.shape[0])]
    #
    #         for j in range(self.distance_matrix.shape[0] - 1):
    #             infinity_edges = set()
    #             for k in range(self.distance_matrix.shape[0]-1):
    #                 if np.isinf(self.distance_matrix[route[-1], k]):
    #                     infinity_edges.add(k)
    #             choices = set(range(self.distance_matrix.shape[0])) - set(route) - infinity_edges
    #             if len(choices) == 0:
    #                 a = [i for i in range(self.distance_matrix.shape[0]) if i not in route]
    #                 random.shuffle(a)
    #                 route = np.concatenate((route, a))
    #                 break
    #             route.append(random.choice(list(choices)))
    #
    #         self.population[i] = Individual(route)
    #         # self.population[i] = Individual(np.random.permutation(self.distance_matrix.shape[0]))
    #
    #     return self.population
    def init_population(self):
        possible_nodes = self.__create_possible_nodes__()
        possible_nodes_arr = [copy.deepcopy(possible_nodes) for i in range(self.population_size)]
        with Pool(processes=self.__processes__) as pool:
            routes = list(pool.map(self.__random_depth_first_search__,possible_nodes_arr))
        for i in range(len(routes)):
            self.population[i] = Individual(routes[i])

    def __create_possible_nodes__(self):
        # Create possible goal nodes for each node, eliminate 'inf' and zero values
        possible_nodes = []
        for i in range(self.distance_matrix.shape[0]):
            possible_nodes.append([])
            for j in range(self.distance_matrix.shape[0]):
                if not (np.isinf(self.distance_matrix[i, j]) or self.distance_matrix[i, j] == 0):
                    possible_nodes[i].append(j)
        return possible_nodes

    def __random_depth_first_search__(self, possible_nodes):

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

    def breed(self, offspring_size, k, mutation_prob):
        with Pool(processes=self.__processes__) as pool:
            offspring = list(pool.starmap(self.__breed_part__, [(k, mutation_prob)]*offspring_size))
        for i in range(len(offspring)):
            offspring[i].cost_function(self.distance_matrix);
        self.population = np.concatenate((self.population, np.array(offspring)))
        self.population_size = len(self.population)

    def elimination(self, new_size, k):
        left_to_eliminate = self.population_size-new_size
        while True:
            with Pool(processes=self.__processes__) as pool:
                results = list(pool.map(self.__k_tournament_elimination__, [k]*left_to_eliminate))
            self.population = np.array([i for i in self.population if list(i.route) not in results])
            self.population_size = len(self.population)
            left_to_eliminate = self.population_size - new_size
            if left_to_eliminate < new_size*0.05:
                break

        if self.population_size != new_size:
            print("new size = " + str(self.population_size))

    def calculate_stats(self):
        # with Pool(processes=self.__processes__) as pool:
        #     pool.starmap(Individual.cost_function, [(i, self.distance_matrix) for i in self.population])

        costs = [self.population[i].cost_function(self.distance_matrix) for i in range(len(self.population))]
        self.best_solution = self.population[costs.index(min(costs))]
        self.mean_objective = np.mean(costs)

    def __breed_part__(self, k, mutation_prob):
        parent1 = self.__k_tournament_selection__(k)
        parent2 = self.__k_tournament_selection__(k)
        offspring = Individual(parent1.edge_crossover(parent2))
        offspring.random_mutation(mutation_prob)
        return offspring

    def __k_tournament_selection__(self, k):
        selected = random.sample(list(self.population), k)
        values = [individual.value for individual in selected]
        return selected[np.argmin(values)]

    def __k_tournament_elimination__(self, k):
        selected = random.sample(list(self.population), k)
        values = [individual.value for individual in selected]
        return list(selected[np.argmax(values)].route)
