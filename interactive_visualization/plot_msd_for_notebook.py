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


def get_translation_fit(path_to_msd, path_to_fit):
    assert os.path.isfile(path_to_msd)
    assert os.path.isfile(path_to_fit)
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
    ax.plot(df_msd.time_ns, df_msd.msd,label="")
    fit = pd.read_csv(path_to_fit)
    p_coeff = [fit["a1"][0], fit["a0"][0]]
    P = np.poly1d(p_coeff)
    ax.plot(df_msd.time_ns, P(df_msd.time_ns), label="D = {:.3e} $m^2/s$".format(1e-10**2/1e-9/6))
    ax.legend()
    #ax.plot(df_msd.time_ns, linear_fit(df_msd.time_ns, *popt))
    # ax.axvline(x=df_msd.time_ns[limit], color='g', linestyle='--', label="fit limit %s"%(limit))
    ax.grid(True)
    return fig, ax
