import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def plot():

    boxplot_data = [[148.5795795795796, 121.44444444444446, 165.2522522522523, 169.08408408408408, 146.2792792792793, 108.23123123123125, 136.22222222222223, 103.21621621621622, 116.72072072072072, 122.09009009009009],
                    [136.23423423423424, 138.97297297297297, 149.55255255255256, 134.93693693693695, 140.5795795795796, 111.15915915915917, 174.73873873873873, 160.16216216216216,106.90390390390391, 128.66366366366367],
                    [127.73273273273273, 88.93093093093094, 95.12612612612614, 141.36636636636638, 154.62762762762765, 153.05405405405406, 115.42342342342343, 143.2762762762763, 100.15915915915917, 88.04204204204206]]
    boxplot_xaxis = ["K-WAY", "Ranked", "Random"]

    # Make the plot of selected checkboxes
    ax = plt.subplot(111)
    plt.boxplot(boxplot_data)
    plt.xticks(fontsize=8)
    ax.set_xticklabels(boxplot_xaxis)
    plt.title("Methods of choosing parents in genetic alogorithm")
    plt.ylabel("Improvement(points)")
    plt.xlabel("Algorithms")
    plt.show()

if __name__ == "__main__":
    plot()
