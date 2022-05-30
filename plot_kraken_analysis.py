#!usr/bin/env python3

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def main():
    cwd = os.getcwd()
    res_path = os.path.join(cwd, "results")

    # data frames
    l29_data_sensitivity = [[],[]]
    l31_data_sensitivity = [[],[]]
    l29_data_ppv = [[],[]]
    l31_data_ppv = [[],[]]

    # read in database parameters and analysis results
    res_dirs = [x for x in os.listdir(res_path) if os.path.isdir(os.path.join(res_path, x))]
    sorted_res_dirs = sorted(res_dirs)
    for dir in sorted_res_dirs:
        res = read_results(os.path.join(res_path, dir, "analysis.txt"))
        k, l, sensitivity, ppv = res[1], res[2], float(res[9].strip("%")), float(res[10].strip("%"))
        if l == "29":
            l29_data_sensitivity[0].append(k)
            l29_data_sensitivity[1].append(sensitivity)
            l29_data_ppv[0].append(k)
            l29_data_ppv[1].append(ppv)
        elif l == "31":
            l31_data_sensitivity[0].append(k)
            l31_data_sensitivity[1].append(sensitivity)
            l31_data_ppv[0].append(k)
            l31_data_ppv[1].append(ppv)

    # plot chart - ax1 = sensitivity chart; ax2 = ppv chart
    fig, ax = plt.subplots()

    line1, = ax.plot(l29_data_sensitivity[0], l29_data_sensitivity[1], label = "l = 29")
    line2, = ax.plot(l31_data_sensitivity[0], l31_data_sensitivity[1], label = "l = 31")
    ax.set_xlabel("k")
    ax.set_ylabel("Sensitivity (%)")
    ax.legend()
    ax.set_title("Kraken2 viral database sensitivity")

    '''line3, = ax2.plot(l29_data_ppv[0], l29_data_ppv[1], label = "l = 29")
    line4, = ax2.plot(l31_data_ppv[0], l31_data_ppv[1], label = "l = 31")
    ax2.set_xlabel("k")
    ax2.set_ylabel("PPV (%)")
    ax2.legend()
    ax2.set_title("Kraken2 viral database PPV")'''

    #fig.tight_layout()
    plt.savefig("analysis.png")

def read_results(filename):
    with open(filename, "r") as r:
        res = r.readlines()[1].strip("\n").split("\t")
    return res

if __name__ == "__main__":
    main()