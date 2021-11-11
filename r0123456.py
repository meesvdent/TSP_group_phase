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
        k = 3
        mutation_prob = 0.1
        iterations = 100
        show_feasible = False

        # Read distance matrix from file.
        file = open(filename)
        distanceMatrix = np.loadtxt(file, delimiter=",")
        # print(distanceMatrix)
        file.close()

        print("Initialization...")
        population = Population(poputation_size, distanceMatrix)
        population.init_population()
        population.calculate_stats()
        if show_feasible:
            cnt = 0
            for i in population.population:
                if not i.is_feasible:
                    cnt += 1
            print("Solutions not feasible= "+str(cnt))
        print("Initialization done")

        while iterations != 0:

            population.breed(offspring_size, k, mutation_prob)
            population.elimination(new_poputation_size, k)
            population.calculate_stats()
            #    with city numbering starting from 0
            timeLeft = self.reporter.report(population.mean_objective, population.best_solution.value, np.array(population.best_solution.route))
            if timeLeft < 0:
                break

            iterations -= 1
            print(iterations)
            if show_feasible:
                cnt = 0
                for i in population.population:
                    if not i.is_feasible:
                        cnt += 1
                print("Solutions not feasible= "+str(cnt))
                print(population.best_solution.is_feasible)
            print("Best value: ", population.best_solution.value)
            print("Mean value: ", population.mean_objective)
        print("timeLeft= "+str(timeLeft))
        return 0


if __name__ == "__main__":
    object = r0123456()
    object.optimize("./data/tour29.csv")
