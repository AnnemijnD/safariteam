import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def plot():


    boxplot_data = [[316.7237237237237, 214.74174174174175, 260.0, 252.07207207207207, 368.34834834834834, 270.07207207207205, 295.07207207207205, 156.72372372372374, 298.0450450450451, 318.34834834834834, 278.0450450450451, 268.0450450450451, 278.34834834834834, 338.34834834834834, 296.6966966966967, 319.34834834834834, 240.35735735735736, 268.7957957957958, 307.05405405405406, 240.37537537537537, 265.4024024024024, 236.6966966966967, 278.6966966966967, 300.7237237237237, 292.34834834834834, 333.7237237237237, 228.34834834834834, 291.3933933933934, 303.34834834834834, 320.02702702702703, 323.6966966966967, 267.0, 253.39339339339338, 315.42042042042044, 247.75075075075074, 238.6966966966967, 277.6966966966967, 270.34834834834834, 264.0810810810811, 210.0, 314.42942942942943, 354.07207207207205, 245.58258258258257, 300.37537537537537, 307.0, 319.37537537537537, 286.07207207207205, 315.37537537537537, 313.3933933933934, 283.0], [222.6966966966967, 297.47447447447445, 252.02702702702703, 228.79579579579578, 343.0900900900901, 246.72372372372374, 279.42942942942943, 273.34834834834834, 278.0450450450451, 276.87687687687685, 256.3933933933934, 353.0, 326.34834834834834, 322.0450450450451, 323.42042042042044, 329.0450450450451, 251.0810810810811, 293.37537537537537, 350.7237237237237, 315.0450450450451, 284.38438438438436, 245.47447447447448, 276.7237237237237, 303.34834834834834, 253.6966966966967, 196.87687687687688, 272.07207207207205, 287.1171171171171, 320.0, 316.6966966966967, 259.6966966966967, 232.07207207207207, 273.3933933933934, 250.04504504504504, 318.54654654654655, 281.7687687687688, 303.38438438438436, 306.3933933933934, 323.3933933933934, 240.0, 313.3933933933934, 297.02702702702703, 262.37537537537537, 252.51951951951952, 303.3663663663664, 358.34834834834834, 335.0450450450451, 252.41141141141142, 263.6966966966967, 187.04504504504504], [315.1261261261261, 270.8408408408408, 309.42942942942943, 319.4834834834835, 343.7237237237237, 304.8048048048048, 308.85885885885887, 324.53753753753756, 331.5735735735736, 268.83183183183183, 341.14414414414415, 319.2072072072072, 330.06306306306305, 303.1261261261261, 341.5015015015015, 307.77777777777777, 336.4114114114114, 308.46546546546546, 337.42042042042044, 283.78678678678676, 308.2072072072072, 255.82282282282281, 306.75975975975973, 322.4834834834835, 305.14414414414415, 326.46546546546546, 278.8048048048048, 327.13513513513516, 323.8408408408408, 329.5195195195195, 304.77777777777777, 313.4834834834835, 317.14414414414415, 347.42042042042044, 338.1981981981982, 332.4384384384384, 309.0810810810811, 304.0990990990991, 353.45645645645646, 317.1801801801802, 326.18918918918916, 349.73273273273276, 345.7957957957958, 348.1081081081081, 292.8048048048048, 310.0900900900901, 319.4834834834835, 333.42042042042044, 328.45645645645646, 347.4474474474475]]

=======
    boxplot_data2 = [[317.6966966966967, 325.0450450450451, 303.6966966966967, 278.6966966966967, 290.0450450450451, 251.6966966966967, 338.34834834834834, 331.8048048048048, 258.6966966966967, 255.7057057057057, 341.37537537537537, 317.02702702702703, 313.0, 323.7237237237237, 306.7237237237237, 242.34834834834834, 298.0, 316.6966966966967, 238.37537537537537, 270.34834834834834, 242.6966966966967, 297.34834834834834, 324.02702702702703, 279.77777777777777, 311.34834834834834, 241.77777777777777, 248.34834834834834, 256.47447447447445, 265.07207207207205, 293.6966966966967, 248.6966966966967, 303.34834834834834, 288.0450450450451, 230.4024024024024, 243.6966966966967, 273.0, 335.37537537537537, 263.0, 190.0], [308.74174174174175, 272.74174174174175, 331.34834834834834, 274.6966966966967, 308.0810810810811, 328.34834834834834, 355.0450450450451, 242.74174174174175, 216.04504504504504, 301.02702702702703, 342.0450450450451, 288.7147147147147, 243.02702702702703, 276.34834834834834, 323.6966966966967, 289.83183183183183, 276.6966966966967, 295.07207207207205, 316.37537537537537, 340.3933933933934, 301.6966966966967, 360.6966966966967, 221.17117117117118, 302.0990990990991, 267.0, 250.02702702702703, 297.0450450450451, 309.0450450450451, 310.5195195195195, 310.02702702702703, 294.05405405405406, 257.02702702702703, 264.0990990990991, 269.3933933933934, 273.4384384384384, 284.47447447447445, 335.1081081081081, 225.018018018018, 238.34834834834834] , [338.7687687687688, 326.8138138138138, 332.8498498498499, 296.8498498498499, 325.5285285285285, 348.4384384384384, 302.8858858858859, 341.8948948948949, 293.85885885885887, 338.4114114114114, 316.8138138138138, 309.78678678678676, 294.5015015015015, 302.8048048048048, 338.7237237237237, 321.5645645645646, 327.14414414414415, 319.8048048048048, 305.1081081081081, 341.0810810810811, 342.42942942942943, 342.75975975975973, 336.7237237237237, 311.4474474474475, 345.4924924924925, 311.14414414414415, 281.4384384384384, 315.82282282282284, 295.55555555555554, 281.0990990990991, 329.54654654654655, 338.75075075075074, 333.8138138138138, 280.4024024024024, 321.4114114114114, 317.2522522522523, 317.1171171171171, 305.74174174174175, 323.4834834834835]]
    boxplot_xaxis = ["Hill climber", "Hill climber extended", "Simulated annealing"]


    # Make the plot of selected checkboxes
    ax = plt.subplot(111)
    plt.boxplot(boxplot_data)
    plt.xticks(fontsize=8)
    ax.set_xticklabels(boxplot_xaxis)
    plt.title("Comparsion of different algorithms")
    plt.ylabel("Points")
    plt.xlabel("Algorithms")
    plt.show()

if __name__ == "__main__":
    plot()
