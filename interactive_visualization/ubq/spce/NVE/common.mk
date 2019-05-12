.EXPORT_ALL_VARIABLES:
.PHONY: all clean

N_RESIDUES:=$(shell python ${SCRIPT_DIR}/makefile_config.py --n-residues)
FIRST_CH3_RESIDUES:=$(shell python ${SCRIPT_DIR}/makefile_config.py --first-ch3-residue)
LAST_CH3_RESIDUES:=$(shell python ${SCRIPT_DIR}/makefile_config.py --last-ch3-residue)
TRAJECTORY_LENGTH:=$(shell python ${SCRIPT_DIR}/makefile_config.py --trajectory-length)
TRAJECTORY_PATH:=$(shell python ${SCRIPT_DIR}/makefile_config.py --trajectory-path)
VOLUME_FILE:=$(shell python ${SCRIPT_DIR}/makefile_config.py --volume-file)
LATTICE_RST7_FILE:=$(shell python ${SCRIPT_DIR}/makefile_config.py --lattice-rst7-file)

PYTHONPATH:=${SCRIPT_DIR}/..
