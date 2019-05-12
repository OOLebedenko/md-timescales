include ${SCRIPT_DIR}/../analysis_template/common.mk

all: figures/tau_2_exp.pdf figures/tau_4_exp.pdf

clean:
	rm -rf data 
	rm -rf figures


figures/tau_2_exp.pdf figures/tau_4_exp.pdf: ${SCRIPT_DIR}/plot_vector_autocorr.py data/fit/tau_2_exp.csv data/fit/tau_4_exp.csv
	mkdir -p figures
	python3 "$<" \
		--path-to-fit=data/fit/ \
		--path-to-acorrs=data/acorr/ \
		--output-directory=figures \
		--vectors-group=CH3


data/fit/tau_2_exp.csv data/fit/tau_4_exp.csv: ${SCRIPT_DIR}/fit_vector_acorr.py data/acorr/${FIRST_CH3_RESIDUES}.csv data/acorr/${LAST_CH3_RESIDUES}.csv
	mkdir -p data/fit/
	python3 "$<" \
		--output-directory=data/fit/ \
		--path-to-acorrs=data/acorr/ \
		--path-to-trajectory="${TRAJECTORY_PATH}" \
		--vectors-group=CH3


data/acorr/${FIRST_CH3_RESIDUES}.csv data/acorr/${LAST_CH3_RESIDUES}.csv:  ${SCRIPT_DIR}/extract_autocorr.py
	mkdir -p data/acorr/
	python3 "$<" \
		--output-directory=data/acorr/ \
		--trajectory-length="${TRAJECTORY_LENGTH}" \
		--path-to-trajectory="${TRAJECTORY_PATH}" \
		--vectors-group=CH3