import os
import matplotlib.pyplot as plt

def plot_hist(folder_path, out_name):
    """
    creates histogram with best and mean value for the solutions with the same parameter set

    :param folder containing results of algorithm with same parameter set
    :return: None
    """
    mean_values = []
    best_values = []

    filenames = os.listdir(folder_path)
    filenames = [folder_path + file for file in filenames]

    for file in filenames:
        data = pd.read_csv(file, delimiter=",", skiprows=2, header=None)
        mean_values.append(data[2][-1])
        best_values.append(data[3][-1])

    plt.hist(best_values)
    plt.hist(mean_values)
    plt.savefig(out_name)


if __name__ == "__main__":
    plot_hist("./out/parameter_set_1", "./out/parameter_set_1/hist.png")
