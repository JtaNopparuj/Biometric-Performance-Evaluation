import numpy as np
import matplotlib.pyplot as plt
import argparse
import logging
from glob import glob
from plot_FAR_FRR import getFARFRR


def figureSettingsROC():
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(which='both')
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    ax.set_xlabel("FMR", fontweight="bold", fontsize=16)
    ax.set_ylabel("TPR", fontweight="bold", fontsize=16)
    ax.set_title("ROC curve", fontweight="bold", fontsize=16)

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    
    return fig, ax

def plotROCcurve(FAR_list, FRR_list):

    fig, ax = figureSettingsROC()
    ax.plot(FAR_list, 1-np.array(FRR_list))

def main(csv_dir):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    csv_path_list = glob(csv_dir + "\*.csv")

    logging.info("Finding FAR & FRR ...")
    FAR_list, FRR_list, T_list = getFARFRR(csv_path_list)

    plotROCcurve(FAR_list, FRR_list)
    logging.info("Done")
    plt.show()

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--match_csv", type=str, required=True, help="Match result (.csv) directory")
    args = vars(ap.parse_args())

    main(args["match_csv"])

