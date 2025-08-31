import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
from glob import glob

def getGenuineImposterScore(csv_path_list):

    genuine_score_list = []
    imposter_score_list = []

    for csv_path in csv_path_list:
        
        match_df = pd.read_csv(csv_path)
        probe_name = csv_path.split('\\')[-1].split('.')[0]
        score_list = match_df["Score"].to_list()

        ##################################################################

        probe_id = probe_name[:3]
        idx = np.where(match_df["Gallery"].to_numpy() == probe_id)[0][0]

        ##################################################################

        genuine_score = score_list.pop(idx)
        genuine_score_list.append(genuine_score)

        imposter_score_list += score_list
    
    return genuine_score_list, imposter_score_list

def plotDistribution(csv_path_list, norm_flag):

    genuine_score_list, imposter_score_list = getGenuineImposterScore(csv_path_list)

    uniq_genuine_score, genuine_counts = np.unique(genuine_score_list, return_counts=True)
    uniq_imposter_score, imposter_counts = np.unique(imposter_score_list, return_counts=True)

    if norm_flag:
        genuine_counts = genuine_counts/len(genuine_score_list)
        imposter_counts = imposter_counts/len(imposter_score_list)

    plt.figure()
    plt.bar(uniq_genuine_score, genuine_counts, color='b', width=1, alpha=0.6, label="Genuine")
    plt.bar(uniq_imposter_score, imposter_counts, color='r', width=1, alpha=0.6, label="Imposter")
    plt.title("Genuine-Imposter Distribution")
    plt.xlabel("Matching Score")
    if norm_flag:
        plt.ylabel("Probability")
    else:
        plt.ylabel("Counts")
    plt.legend()
    plt.grid()
    plt.show()

def main(csv_dir, norm_flag):

    csv_path_list = glob(csv_dir + "\*.csv")
    plotDistribution(csv_path_list, norm_flag)


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--match_csv", type=str, required=True, help="Match result (.csv) directory")
    ap.add_argument("-norm", "--norm_flag", type=int, required=False, default=1, help="Normalization Flag")
    args = vars(ap.parse_args())

    main(args["match_csv"], args["norm_flag"])


