import numpy as np
import pandas as pd
import argparse
import logging
import os
import matplotlib.pyplot as plt
from glob import glob

def identify(csv_path_list):

    iden_df = pd.DataFrame(columns=["Probe", "Rank", "Score"])
    
    for csv_path in csv_path_list:

        df = pd.read_csv(csv_path)
        probe_name = csv_path.split('\\')[-1].split('.')[0]

        probe_id = probe_name[:3]
        idx = np.where(df["Gallery"].to_numpy() == probe_id)[0][0]

        rank = idx + 1 # -> Rank start with 1 but index start with 0
        score = df["Score"].to_numpy()[idx]

        iden_df.loc[len(iden_df)] = [probe_name, rank, score]

    return iden_df

def getIdenRate(df, Max_bound_rank=30):

    probe_rank_list = df['Rank'].to_list()
    Iden_rate = []
    Init_idenRate = 0
    for i in range(1,Max_bound_rank+1):
        Init_idenRate += probe_rank_list.count(i)
        Rank_idenRate = 100*Init_idenRate/len(probe_rank_list)
        Iden_rate.append(Rank_idenRate)
    return Iden_rate

def figureSettingsCMC(max_rank):
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(1, 1, 1)

    # -> Set grid interval
    x_major_ticks = np.arange(0, max_rank+1, 5)
    x_minor_ticks = np.arange(0, max_rank+1, 1)
    y_major_ticks = np.arange(0, 101, 5)
    y_minor_ticks = np.arange(0, 101, 1)
    ax.set_xticks(x_major_ticks)
    ax.set_xticks(x_minor_ticks, minor=True)
    ax.set_yticks(y_major_ticks)
    ax.set_yticks(y_minor_ticks, minor=True)
    ax.grid(which='both')
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    ax.set_xlim(1,max_rank)

    # -> Other settings
    ax.set_xlabel("Rank", fontweight="bold", fontsize=16)
    ax.set_ylabel("Identification Rate (%)", fontweight="bold", fontsize=16)
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14

    ax.set_title("CMC curve", fontweight="bold", fontsize=16)
    
    return fig, ax

def plotCMCcurve(IdenRate, max_rank):

    fig, ax = figureSettingsCMC(max_rank)
    
    min_idenRate = int(min(IdenRate))
    max_idenRate = int(max(IdenRate))

    lower_ylim = min_idenRate - 5
    upper_ylim = max_idenRate + 5
    if upper_ylim >= 101:
        upper_ylim = 101
    ax.set_ylim(lower_ylim, upper_ylim)

    # -> Plot
    Rank_axis = np.arange(1, max_rank+1)

    ax.plot(Rank_axis, IdenRate, 'bo-')

def main(csv_dir, max_rank, save_flag, output_dir):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    csv_path_list = glob(csv_dir + "\*.csv")

    logging.info("Identify ...")
    iden_df = identify(csv_path_list)

    if save_flag:
        logging.info("Saving csv ...")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "rank.csv")
        iden_df.to_csv(output_path, index=False)

    logging.info("Computing Identification Rate ...")
    iden_rate = getIdenRate(iden_df, max_rank)

    plotCMCcurve(iden_rate, max_rank)
    logging.info("Done")
    plt.show()

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--match_csv", type=str, required=True, help="Match result (.csv) directory")
    ap.add_argument("-maxr", "--max_rank", type=int, required=False, default=30, help="Maximum Rank")
    ap.add_argument("-s", "--save_csv", type=int, required=False, default=0, help="Save .csv")
    ap.add_argument("-o", "--csv_outdir", type=str, required=False, default=r"../output", help="Output .csv Directory")
    args = vars(ap.parse_args())

    main(args["match_csv"], args["max_rank"], args["save_csv"], args["csv_outdir"])


