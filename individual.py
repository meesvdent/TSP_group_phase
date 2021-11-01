"""
Individual class, holds an individual route
"""

import numpy as np


class Individual:

    def __init__(self, route):
        self.route = np.array(route)
        self.value = 0

    def __repr__(self):
        return str(self.route)

    def cost_function(self, distances):
        self.value = 0
        for i in range(len(self.route)-1):
            from_city = self.route[i]
            to_city = self.route[i+1]
            self.value += distances[from_city, to_city]
        self.value += distances[-1, 0]
        return self.value

    def edge_crossover(self, parent2):
        # create edge table
        edge_table = [[] for i in range(len(self.route))]
        for i in range(len(self.route)):
            pos1 = i+1
            if pos1 >= len(self.route):
                pos1 = 0
            edge_table[self.route[i]-1].append(self.route[i-1])
            edge_table[self.route[i]-1].append(self.route[pos1])
            # print(edge_table)
            # print("\n")

            pos2 = np.where(parent2.route == self.route[i])[0][0] + 1
            if pos2 >= len(self.route):
                pos2 = 0
            edge_table[self.route[i]-1].append(parent2.route[np.where(parent2.route == self.route[i])[0][0]-1])
            edge_table[self.route[i]-1].append(parent2.route[pos2])

        offspring = []
        # start from a random
        offspring.append(1)#self.route[np.random.randint(len(self.route))+1])
        current_element = offspring[0]
        print(offspring)
        print("\n")


        reverse = False
        while len(offspring) < len(self.route):
            #remove current_element from all
            for i in range(len(self.route)):
                while current_element in edge_table[i]:
                    edge_table[i].remove(current_element)

            print(edge_table)

            if len(edge_table[current_element-1]) == 0:
                if reverse:
                    not_visited = list(set(self.route) - set(offspring))
                    current_element = not_visited[np.random.randint(len(not_visited))]+1
                    offspring.append(current_element)
                else:
                    current_element = offspring[0]
                    offspring = offspring.reverse()
                    reverse = True
            else:
                duplicate = False
                for j in edge_table[current_element-1]:
                    if edge_table[current_element-1].count(j) == 2:
                        current_element = j
                        duplicate = True
                if not duplicate:
                    list_len = [len(set(edge_table[i-1])) for i in edge_table[current_element-1]]
                    current_element = edge_table[current_element-1][list_len.index(min(list_len))]
                offspring.append(current_element)
                print(offspring)
                print("\n")

        return offspring
