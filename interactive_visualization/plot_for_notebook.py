import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import os
from matplotlib.backends.backend_pdf import PdfPages
from typing import *


def __multi_exp_f(x: Union[float, int],
                  A: List[Union[float, int]],
                  TAU: List[Union[float, int]],
                  C: Union[float, int]) -> float:
    """
    :param x: argument of some exponential functions composition
    :param A: array of amplitudes
    :param TAU: array of time constants
    :param C: free element
    :return: sum exponential functions composition
    """
    return np.sum(
        (a * np.exp(-x / tau)) for a, tau in zip(A, TAU)
    ) + C

def __get_autocorr_graph_label(fit_line):
    amplitude = fit_line.filter(like='-a')
    tau = fit_line.filter(like='-tau')
    union_a_tau = ["{a_label:2s} = {a_value:5.3f} ; {tau_label:3s} = {tau_value:8.3e}".format(
        a_label=a_label,
        a_value=fit_line[a_label],
        tau_label=tau_label,
        tau_value=fit_line[tau_label])
        for a_label, tau_label in zip(amplitude.index.tolist(), tau.index.tolist())
    ]
    if fit_line['aName'][0] == "C":
        union_a_tau.append(" ; {constant_label:3s} = {constant:5.3f}".format(
            constant=fit_line['constant'],
            constant_label="C"))
    graph_label = "\n".join(union_a_tau)
    return graph_label


def settings_plot(graph_label):
    left, width = .40, .54
    bottom, height = .40, .54
    right = left + width
    top = bottom + height
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.text(right, top, graph_label,
            horizontalalignment='right',
            verticalalignment='top',
            transform=ax.transAxes,
            multialignment='left',
            bbox={'facecolor': 'moccasin', 'alpha': 0.5, 'pad': 6})
    ax.set_xlabel('time, ns', fontsize=13)
    ax.set_ylabel('C(t)', fontsize=13)
    ax.grid(True)
    return fig, ax


def plot_figure_autocorr(time, fit_line, acorr):
    amplitude = fit_line.filter(like='-a')
    tau = fit_line.filter(like='-tau')
    if fit_line['aName'][0] == "C":
        constant = fit_line['constant']
    else:
        constant = 0
    order = len(amplitude)
    rid = fit_line["rId"]
    rname = fit_line["rName"]
    aname = fit_line["aName"]
    limit = fit_line["limit"]

    graph_label = __get_autocorr_graph_label(fit_line)
    fig, ax = settings_plot(graph_label)
    if aname == "N":
        ax.set_title('NH autocorrelation plot %d exp %s %s' % (order, rid, rname))
        ax.set_xlim(-1, 20)
    elif aname[0] == "C":
        ax.set_title('CH3 autocorrelation plot %d exp %s %s %s' % (order, rid, rname, aname))
        ax.set_xlim(-0.05, 2)
    ax.set_ylim(-0.1, 1.1)
    ax.plot(time, acorr)
    ax.plot(time, __multi_exp_f(time, amplitude,
                                tau, C=constant))
    ax.axvline(x=time[limit], color='g', linestyle='--')
    return fig, ax


def get_plot_acorr_fit(path_to_fit_csv: str,
                       path_to_csv_acorr: str,
                       order: int, 
                       ind) -> None:
    """
    Plot one pdf with a particular fit function (e.g. tau-2-exp.pdf)

    :param path_to_fit_csv: path to particular fit
           function values (e.g. tau-2-exp.csv) files
    :param path_to_csv_acorr: path to two-column .csv files [time_ns, acorr]
    :param output_directory: path to fit pdf with
           a particular fit function (e.g. tau-2-exp.pdf)
    """
    exp_order = {2: "tau_2_exp", 3: "tau_3_exp", 4: "tau_4_exp"}
    csv_fit = os.path.join(path_to_fit_csv, exp_order[order] + ".csv")
    fit = pd.read_csv(csv_fit)
    fit_line = fit.iloc[ind]
    # file = "{}/{:02d}_{}.csv".format(path_to_csv_acorr, fit_line["rId"], fit_line["aName"])
    df = pd.read_csv(path_to_csv_acorr)
    fig, ax = plot_figure_autocorr(df.time_ns, fit_line, df.acorr)
    return fig, ax
    
