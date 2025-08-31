import numpy as np
import matplotlib.pyplot as plt
import argparse
import logging
from glob import glob
from scipy.optimize import brentq
from scipy.interpolate import interp1d
from plot_genuine_imposter import getGenuineImposterScore

def getFARFRR(csv_path_list):
    
    genuine_score_list, imposter_score_list = getGenuineImposterScore(csv_path_list)

    T_min = int(min(np.array(genuine_score_list).min(), np.array(imposter_score_list).min()))
    T_max = int(max(np.array(genuine_score_list).max(), np.array(imposter_score_list).max()))
    T_list = np.arange(T_min, T_max+1)

    FAR_list = []   # -> FMR
    FRR_list = []   # -> FNMR

    ### -> Find FAR, FRR for each Threshold
    for T in T_list:
        
        FAR = np.sum(imposter_score_list>=T) / len(imposter_score_list)
        FRR = np.sum(genuine_score_list<T) / len(genuine_score_list)

        FAR_list.append(FAR)
        FRR_list.append(FRR)

    return FAR_list, FRR_list, T_list

def figureSettingsFARFRR():
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel("Threshold", fontweight="bold", fontsize=16)
    ax.set_ylabel("Error Rate", fontweight="bold", fontsize=16)
    ax.set_title("FAR-FRR Curve", fontweight="bold", fontsize=16)
    ax.set_ylim(0, 1)

    ax.grid(which='both')
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    return fig, ax


def findEER(FAR_list, FRR_list, T_list):

    FAR_intp_list = interp1d(T_list, FAR_list)
    FRR_intp_list = interp1d(T_list, FRR_list)
 
    EER_threshold = brentq(lambda x: FAR_intp_list(x) - FRR_intp_list(x),
                           T_list[0], T_list[-1])
    EER = FAR_intp_list(EER_threshold)
    return EER, EER_threshold

def plotFARFRR(FAR_list, FRR_list, T_list, EER, EER_threshold):

    fig, ax = figureSettingsFARFRR()
    ax.plot(T_list, FAR_list, label="FAR")
    ax.plot(T_list, FRR_list, label="FRR")
    ax.plot(EER_threshold, EER, 'ro', label=f"EER = {EER:.6f}")

    ax.axvline(EER_threshold, color='green', linestyle='--', alpha=0.5)
    ax.axhline(EER, color='green', linestyle='--', alpha=0.5)
    ax.legend(loc='lower right')
    ax.set_xlim(T_list[0],T_list[-1])

def main(csv_dir):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    csv_path_list = glob(csv_dir + "\*.csv")

    logging.info("Finding FAR & FRR ...")
    FAR_list, FRR_list, T_list = getFARFRR(csv_path_list)

    logging.info("Computing EER ...")
    EER, EER_threshold = findEER(FAR_list, FRR_list, T_list)

    plotFARFRR(FAR_list, FRR_list, T_list, EER, EER_threshold)
    logging.info("Done")
    plt.show()

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--match_csv", type=str, required=True, help="Match result (.csv) directory")
    args = vars(ap.parse_args())

    main(args["match_csv"])

