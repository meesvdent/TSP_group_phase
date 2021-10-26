from individual import Individual
from population import Population

import numpy as np

def test_individual():
    order = list(range(10))
    test_ind = Individual(order)

    order[5] = 10

def test_population():
    dist_matrix = test_file('tour29.csv')
    pop_one = Population(100, dist_matrix)


def test_file(filename):
    file = open(filename)
    distanceMatrix = np.loadtxt(file, delimiter=",")
    file.close()
    return distanceMatrix

def test_k_tournament():
    dist_matrix = test_file('tour29.csv')
    pop_two = Population(100, dist_matrix)
    pop_two.init_population()
    print("k tournament")
    print(pop_two.k_tournament(5))

if __name__ == "__main__":
    test_individual()
    test_file('tour29.csv')
    test_population()
    test_k_tournament()


