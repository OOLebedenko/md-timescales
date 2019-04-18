import argparse
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import os
from matplotlib.backends.backend_pdf import PdfPages


def mono_exp(x, a1, tau1):
    return a1 * np.exp(-x / tau1)


def plot_acorr_fit(path_to_fit_csv, path_to_csv_acorr, path_to_output_pdf):
    """
    Plot one pdf with a particular fit function (e.g. inertia_tensor-acorr-2-exp.pdf)
     - [ ] Show acorr data
     - [ ] Show fit curve
     - [ ] Show fit parameters
     - [ ] Denote fit region by vertical line
    """
    with PdfPages(os.path.join(path_to_output_pdf, "overall_tumbling.pdf")) as pdf:
        csv_fit = glob.glob(os.path.join(path_to_fit_csv, "*.csv"))[0]
        fit = pd.read_csv(csv_fit)
        order = 1
        for i, fit_line in fit.iterrows():
            inertia_axis = fit_line["axis"]
            df = pd.read_csv(os.path.join(path_to_csv_acorr, "tumbling_%s.csv" % (inertia_axis)))
            amplitude_label = ["exp-%d-a%d" % (order, i + 1) for i in range(order)]
            tau_label = ["exp-%d-tau%d" % (order, i + 1) for i in range(order)]
            popt = {"a%d" % (i + 1): fit_line[amplitude_label[i]] for i in range(order)}
            tau = {"tau%d" % (i + 1): fit_line[tau_label[i]] for i in range(order)}
            popt.update(tau)

            limit = fit_line["limit"]
            coeff_a = ["a%d" % (i + 1) for i in range(order)]
            coeff_tau = ["tau%d" % (i + 1) for i in range(order)]
            union_a_tau = [r"$\tau$ = {tau_value:8.3e} ns".format(
                a_label=a_label,
                a_value=popt[a_label],
                tau_label=tau_label,
                tau_value=popt[tau_label])
                for a_label, tau_label in zip(coeff_a, coeff_tau)
            ]
            graph_label = "\n".join(union_a_tau)
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
            ax.set_ylim(-0.1, 1.1)
            ax.set_xlim(-1, 20)
            ax.set_xlabel('time, ns', fontsize=13)
            ax.set_ylabel('autocorrelation', fontsize=13)
            ax.set_title('inertia_tensor autocorrelation plot %s axis %d exp' % (inertia_axis, order))
            ax.plot(df.time_ns, df.acorr)
            ax.plot(df.time_ns, mono_exp(df.time_ns, **popt))
            ax.axvline(x=df.time_ns[limit], color='g', linestyle='--', label="fit limit %s" % (limit))
            ax.grid(True)
            # ax.set_legend(("inertia_tensor autocorrelation", "fit , loc='upper right')
            pdf.savefig()
            plt.close()


if __name__ == "__main__":
    # -f_csv "/home/legosta/bioinf/scripts/md-timescales/md_timescales" -a_csv "/home/legosta/bioinf/scripts/data/acorr"
    parser = argparse.ArgumentParser(description="plot inertia_tensor autocorrelation")
    parser.add_argument('-f_csv', '--path-to-fit', required=True)
    parser.add_argument('-a_csv', '--path-to-acorrs', required=True)
    parser.add_argument('-o', '--output-directory', default=os.getcwd())
    args = parser.parse_args()
plot_acorr_fit(args.path_to_fit, args.path_to_acorrs, args.output_directory)
