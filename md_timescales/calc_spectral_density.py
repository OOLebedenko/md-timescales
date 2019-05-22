import argparse
import pandas as pd 
import numpy as np
import os


def calc_spectral_density(path_to_fit_csv, w):
    df = pd.read_csv(path_to_fit_csv)
    density_table = pd.DataFrame()
    for ind,fit_line in df.iterrows():
        amplitude = fit_line.filter(like='-a')
        taus = fit_line.filter(like='-tau')
        if fit_line['aName'][0] == "C":
            constant=fit_line['constant']
        else:
            C = 0
        order = len(amplitude)
        density = sum(
            (a * tau/(1+np.square(tau*w))) for a, tau in zip(amplitude, taus)
        ) + C
        D = {'rName': df.rName[ind], 'aName': df.aName[ind], 'rId': df.rId[ind], 'density_{order}_exp'.format(order=order): density}
        temp = pd.DataFrame(D, index=[0])
        density_table = pd.concat([density_table, temp])
    return density_table


def get_spectral_density(path_to_fit, w, output_directory):
    df = pd.DataFrame()
    fits = ["tau_2_exp.csv", "tau_3_exp.csv", "tau_4_exp.csv"]
    for fit in fits:
        path_to_fit_csv = os.path.join(path_to_fit, fit)
        density_for_csv_fit = calc_spectral_density(path_to_fit_csv, w)
        if df.empty:
            df = density_for_csv_fit
        else:
            df = pd.merge(df,density_for_csv_fit, left_index=False, right_index=False)
            df.to_csv(os.path.join(output_directory, "Spectral_density.csv"))
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculation of spectral density')
    parser.add_argument('--path-to-fit-csv', required=True, )
    parser.add_argument('--frequency', type=int, required=True)
    parser.add_argument('--output-directory', default="./")
    args = parser.parse_args()
    get_spectral_density(args.path_to_fit_csv, args.frequency, args.output_directory)
    #python3 calc_spectral_density.py --path-to-fit-csv ../../handling_stas/handling/ubq/spce/NVE/autocorr/NH/data/fit/ --frequency 500
