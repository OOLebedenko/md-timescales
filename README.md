# Influence of molecular dynamics parameters on the timescales characteristic motions of proteins

## Project description

In this repository we present steps of extraction timescales characteristic of biomolecules motion in Molecular Dynamics (MD) modeling.
MD modeling of biomolecules is one of the most important and promising tools of structural biology. 
As a rule, this kind of research uses the NPT ensemble (fixed pressure P, temperature T, and number of atoms N) for modeling. 
However, the use of NPT with a standard set of parameters of the barostat and thermostat leads to a significant slowdown in the dynamics.
In the present study we investigated influence of water model parameters (spce, tip3p, tip4p-d, tip4p-ew) and
and ensemble (NVE, NVT, NPT gamma_ln=0.01,  NPT gamma_ln=2) on characteristic times of rotation and translation globular protein ubiquitin and disordered peptide - N-terminal domain histone h4

## Goals and objectives

The aim of the project: determination of optimal parameters MD on the example of globular protein - ubiquitin (ubq) and
disordered peptide - N-terminal domain histone H4 (h4) for correct modeling timescales characteristic motions of proteins

1) Handling molecular dynamics trajectory, which are obtained for water model parameters (spce, tip3p, tip4p-d, tip4p-ew) and
and ensemble (NVE, NVT, NPT gamma_ln=0.01,  NPT gamma_ln=2) in Amber ff14SB force field for ubq and h4
2) Definition of characteristic times of rotation globular protein (ubq)
3) Definition of characteristic times of translational diffusion globular protein (ubq) and disordered peptide (N-terminal domain h4)
4) Comparison result of MD simulation with experimental values

## Methods


### Scripts description
Code of the project may be divided in two principal parts. 
First part is set of python scripts for extraction, fit and plot timescales characteristic of biomolecules motion. 
Scripts may be used for analysing three types of motions: autocorrelation NH or CH3 groups, translational diffusion and rotational diffusion (overall thumbling)
Second part includes makefiles for handling every types of motions from MD trajectory for ubq and h4. It is assumed that trajectory files has the fixed organization
protein(h4,ubq)/water_model(spce,tip3p,tip4p-d,tip4p-ew)/ensemble(NVE,NVT,NPT_gamma_ln_0.01, NPT_gamma_ln_2)

[**Scripts**](https://github.com/OOLebedenko/md-timescales/tree/master/md_timescales)
 
1) Extraction part

  - extract.py - set of library scripts for extraction autocorrelation function NH or CH3 groups, 
             average autocorrelation function for set of vectors isotropic distributed over the spherical surface for rotational diffusion (overall thumbling),
             mean square displacement (msd) for translational diffusion
  - calc.py - library scripts for calculation mean square displacement (msd)
  - extract_autocorr.py - command-line interfaces for extraction autocorrelation function NH or CH3 groups
  - extract_inertia_tensor_vectors_autocorr.py - command-line interfaces for extraction overall thumbling 
  - extract_mass_center.py - command-line interfaces for extraction mass center coordinates
  - calc_msd.py - command-line interfaces for calculation msd

2) Fit part

  - fit.py - set of library scripts for fit autocorrelation function NH or CH3 groups, translational diffusion and rotational diffusion from MD trajectory
  - fit_vector_acorr.py - command-line interfaces for fit autocorrelation function NH or CH3 groups
  - fit_overall_tumbling.py - command-line interfaces fit extraction overall thumbling autocorrelation function
  - fit_msd.py - command-line interfaces for fit mean square displacement


3) Plot part

  - plot.py - - set of library scripts for fit autocorrelation NH or CH3 groups, translational diffusion and rotational diffusion from MD trajectory
  - plot_vector_acorr.py - command-line interfaces for plot autocorrelation function NH or CH3 groups and fit
  - plot_overall_tumbling.py - command-line interfaces for plot ooverall thumbling autocorrelation function and fit
  - plot_msd.py - command-line interfaces for plot mean square displacement and fit
  

[**Analysis template**](https://github.com/OOLebedenko/md-timescales/tree/master/analysis_template)

  - makefile - main global makefile for run all types of analysis
  - common.mk - main global configuration file 
  - autocorr - directory with makefiles for autocorrelation analysis
  - translational_diffusion - directory with makefiles for translational diffusion analysis
  
## Current results 

  - 15 from 32 trajectories were complete analysed
  - All complete analyzed trajectories of molecular dynamics are not reproduce the experimental value coefficient of translational diffusion for ubq
    MD trajectory with parameters:

| water model | ansamble |
| ------ | ------ |
| spce | NVE |
| tip4p-ew | NVE |
| tip4p-ew | NPT gamma ln 2 |
| tip4p-d | NVE |

consistent with experimental value coefficient of rotational diffusion  for ubq

### Translational diffusion coefficient for ubq. Red line shows experimental value
  ![](https://drive.google.com/uc?id=1m9XW8D_e406Ie20i87MWloMDXhuB0uyG)
### Translational diffusion coefficient for h4
  ![](https://drive.google.com/uc?id=1QLTAvWWf9etNZ532kfSH-ZhGawSLgCjb)
### Rotational diffusion coefficient for ubq. Red line shows experimental value
  ![](https://drive.google.com/uc?id=1Zf_LbIMv9xi2mqDink7YKs7-gI3kAJqU)



