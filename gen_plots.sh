#!/bin/bash

source env.sh

experiment=$1

if [ "${experiment}" = "fig_01" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_01.sh
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_01 
elif [ "${experiment}" = "fig_02" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_02.sh
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_02 
elif [ "${experiment}" = "fig_03" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_02.sh
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_03 
elif [ "${experiment}" = "fig_04" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_04.sh
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_04 
elif [ "${experiment}" = "fig_08" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_08.sh
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_08 
elif [ "${experiment}" = "fig_09" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_08.sh
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_09 
elif [ "${experiment}" = "fig_10" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_08.sh
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_10 
elif [ "${experiment}" = "fig_11" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_11.sh
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_11 
elif [ "${experiment}" = "fig_12" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_12.sh
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_12 
elif [ "${experiment}" = "fig_13" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_13.sh
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_13 
elif [ "${experiemnt}" == "AE"]; then
	echo "Parsing data..."
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_08.sh
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_11.sh
	echo "Generating AE plots..."
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_08 
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_09 
elif [ "${experiments}" == "all" ]; then
	echo "Parsing data..."
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_01.sh
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_02.sh
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_08.sh
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_11.sh
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_12.sh
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_13.sh
	echo "Generating all plots..."
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_01 
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_03 
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_08 
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_09 
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_10 
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_11 
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_12 
	python3 ${ROOT_DIR}/scripts/gen_plots.py --figure fig_13 
else 
	echo "There is no option avaiable for ${experiments}." 
fi

