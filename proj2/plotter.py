import matplotlib.pyplot as plt
import math
import numpy as np
if __name__ == "__main__":
    convex_hull = [0, 0.000505543, 0.002607012, 0.026966286, 0.331895685, 1.916521072, 3.957089949]
    ch = [i * 3 for i in convex_hull]
    n_2 = [i**2 for i in range(1,8)]
    log = [i * math.log(i) for i in range(1, 8)]
    fig, ax = plt.subplots()
    # x = np.linspace()
    x = np.linspace(0, 1000000, 7)

    plt.plot(x, ch, label='convex hull')
    plt.plot(x, n_2, label='n^2')
    plt.plot(x, log, label='log')

    plt.xlabel("n")
    plt.ylabel("t")
    plt.title("Convex Hull Analysis")
    ax.set_xscale('log')
    plt.show()
