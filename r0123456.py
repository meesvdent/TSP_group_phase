import Reporter
import numpy as np
from population import Population


# Modify the class name to match your student number.
class r0123456:

    def __init__(self):
        self.reporter = Reporter.Reporter(self.__class__.__name__)

    # The evolutionary algorithm's main loop
    def optimize(self, filename):

        poputation_size = 500
        new_poputation_size = 500
        offspring_size = 500
        k = 10
        mutation_prob = 0.05
        iterations = 50

        # Read distance matrix from file.
        file = open(filename)
        distanceMatrix = np.loadtxt(file, delimiter=",")
        # print(distanceMatrix)
        file.close()

        population = Population(poputation_size, distanceMatrix)
        population.init_population()

        while iterations != 0:

            population.breed(offspring_size, k, mutation_prob)
            population.elimination(new_poputation_size, k)
            population.calculate_stats()
            #    with city numbering starting from 0
            timeLeft = self.reporter.report(population.mean_objective, population.best_solution.value, np.array(population.best_solution.route))
            if timeLeft < 0:
                break

            iterations -= 1
            print("Iteration: ", iterations)
            print("Best solution is feasible: ", population.best_solution.is_feasible)
            print("Best solution cost: ", population.best_solution.value)
            print("Mean solution: ", population.mean_objective)
        return 0


if __name__ == "__main__":
    object = r0123456()
    object.optimize("./data/tour100.csv")
