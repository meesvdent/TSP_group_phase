import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_value(filename):
    data = pd.read_csv(filename, delimiter=",", skiprows=2, header=None)
    iteration = np.array(data[0])
    best_value = np.array(data[3])
    mean_value = np.array(data[2])

    plt.plot(iteration, best_value, label="Best value")
    plt.plot(iteration, mean_value, label="Mean value")
    plt.show()




if __name__ == "__main__":
    plot_value("1000_1000_1000_3_0_3_100.csv")

