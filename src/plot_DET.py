import numpy as np
import matplotlib.pyplot as plt
import argparse
import logging
from glob import glob
from plot_FAR_FRR import getFARFRR


def figureSettingsDET(log_scale=True):
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(which='both')
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    ax.set_xlabel("FMR", fontweight="bold", fontsize=16)
    ax.set_ylabel("FNMR", fontweight="bold", fontsize=16)
    ax.set_title("DET curve", fontweight="bold", fontsize=16)

    if log_scale:
        ax.set_xscale("log")
        ax.set_yscale("log")
    else:
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 1.02)
    
    return fig, ax

def plotDETcurve(FAR_list, FRR_list, log_scale):

    fig, ax = figureSettingsDET(log_scale)
    ax.plot(FAR_list, FRR_list)

def main(csv_dir, log_scale):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    csv_path_list = glob(csv_dir + "\*.csv")

    logging.info("Finding FAR & FRR ...")
    FAR_list, FRR_list, T_list = getFARFRR(csv_path_list)

    plotDETcurve(FAR_list, FRR_list, log_scale)
    logging.info("Done")
    plt.show()

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--match_csv", type=str, required=True, help="Match result (.csv) directory")
    ap.add_argument("-log", "--log_scale", type=int, required=False, default=1, help="Log Scale Flag")
    args = vars(ap.parse_args())

    main(args["match_csv"], args["log_scale"])

