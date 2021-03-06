from individual import Individual
from population import Population

import numpy as np

def test_individual():
    order = list(range(10))
    test_ind = Individual(order)

    order[5] = 10

def test_population(dist_matrix):
    pop_one = Population(100, dist_matrix)
    pop_one.init_population()
    return pop_one


def test_file(filename):
    file = open(filename)
    distanceMatrix = np.loadtxt(file, delimiter=",")
    file.close()
    return distanceMatrix

def test_k_tournament(population):
    return population.k_tournament(5)


if __name__ == "__main__":
    # test_1 = Individual([1, 2, 3, 4, 5, 6, 7, 8, 9])
    # test_2 = Individual([9, 3, 7, 8, 2, 6, 5, 1, 4])
    # print(test_1.edge_crossover(test_2))
    # test_individual()
    dist_matrix = test_file('./data/tour100.csv')
    test_population = test_population(dist_matrix)
    test_population.depth_first_search()
    # print("K tournament: ")
    # print(test_k_tournament(test_population))
