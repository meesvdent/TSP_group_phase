import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_value(filename, out_name):
    data = pd.read_csv(filename, delimiter=",", skiprows=2, header=None)
    iteration = np.array(data[0])
    best_value = np.array(data[3])
    mean_value = np.array(data[2])

    plt.plot(iteration, best_value, label="Best value")
    plt.plot(iteration, mean_value, label="Mean value")
    plt.savefig(out_name)



if __name__ == "__main__":
    files = os.listdir('./out/parameter_set_1')
    for file in files:
        out_name = file.split('.')[0] + '.png'
        filename = './out/parameter_set_1/' + file
        out_name = './out/parameter_set_1/' + out_name
        plot_value(filename, out_name)

