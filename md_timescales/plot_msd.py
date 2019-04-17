import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np
import glob
import os
from scipy.optimize import curve_fit
from bionmr_utils.md import  *



def fit_limit(data):
    def moving_average(data_set, periods=1):
        weights = np.ones(periods) / periods
        return np.convolve(data_set, weights, mode='valid')
    diff = np.diff(data)
    pos_diff = (diff > 0).astype(int)
    window_size = 30000
    pos_diff_avg = moving_average(pos_diff, window_size)
    index = np.argmax(pos_diff_avg>0.5) + window_size//2
    return index

def linear_fit(x, a1):
    return a1*x


def get_translation_fit(path_to_msd, output_directory): 
    df_msd = pd.read_csv(path_to_msd)
    #popt, pcov = curve_fit(linear_fit, df_msd.time_ns[:limit], df_msd.delta_rsquare[:limit])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # graph_label = "{a1:.2f}".format(a1=popt[0]) + " A^2/ns"
    left, width = .08, .08
    bottom, height = .43, .43
    right = left + width
    top = bottom + height
    # ax.text(right, top, graph_label,
    #     horizontalalignment='left',
    #     verticalalignment='top',
    #     transform=ax.transAxes,
    #     multialignment='left',
    #     bbox={'facecolor': 'moccasin', 'alpha': 0.5, 'pad': 6})
    ax.set_xlabel('time, ns', fontsize = 13)
    ax.set_ylabel('msd, A^2', fontsize = 13)
    ax.set_title('Mean square displacement center mass (msd)')
    ax.plot(df_msd.time_ns, df_msd.delta_rsquare)
    #ax.plot(df_msd.time_ns, linear_fit(df_msd.time_ns, *popt))
    # ax.axvline(x=df_msd.time_ns[limit], color='g', linestyle='--', label="fit limit %s"%(limit))
    ax.grid(True)
    plt.savefig(os.path.join(output_directory, "fit_msd_plot.png"))
    plt.close()
    # return popt



if __name__ == '__main__':	
    # -i "/home/olebedenko/bioinf/scripts/md-timescales/md_timescales/msd.csv -lim 78000"
    parser = argparse.ArgumentParser(description='Plot msd autocorrelation')
    parser.add_argument('--path-to-msd', required=True)
    parser.add_argument('--output-directory', default=os.getcwd())
    args = parser.parse_args()
    get_translation_fit(args.path_to_msd, args.output_directory)