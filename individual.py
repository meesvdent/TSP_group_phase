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
