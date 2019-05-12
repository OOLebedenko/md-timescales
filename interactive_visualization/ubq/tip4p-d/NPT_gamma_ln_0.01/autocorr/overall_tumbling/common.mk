include ${SCRIPT_DIR}/../analysis_template/common.mk


all: figures/overall_tumbling.pdf

clean:
	rm -rf data 
	rm -rf figures





figures/overall_tumbling.pdf: ${SCRIPT_DIR}/plot_overall_tumbling.py data/fit/tau_1_exp.csv
	mkdir -p figures
	python3 $< \
		--path-to-fit=data/fit/ \
		--path-to-acorrs=data/acorr/ \
		--output-directory=figures \



data/fit/tau_1_exp.csv: ${SCRIPT_DIR}/fit_overall_tumbling.py data/acorr/tumbling_x.csv data/acorr/tumbling_z.csv
	mkdir -p data/fit/
	python3 $< \
		--path-to-trajectory="${TRAJECTORY_PATH}" \
		--path-to-acorrs=data/acorr/ \
		--output-directory=data/fit/


data/acorr/tumbling_x.csv data/acorr/tumbling_z.csv: ${SCRIPT_DIR}/extract_inertia_tensor_vectors_autocorr.py
	mkdir -p data/acorr/
	python3 $< \
		--output-directory=data/acorr/ \
		--trajectory-length=${TRAJECTORY_LENGTH} \
		--path-to-trajectory="${TRAJECTORY_PATH}"
