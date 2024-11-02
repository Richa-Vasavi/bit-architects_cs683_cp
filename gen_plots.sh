#!/bin/bash

source env.sh

experiment=$1

if [ "${experiment}" = "fig_01" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_01.sh
elif [ "${experiment}" = "fig_02" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_02.sh
elif [ "${experiment}" = "fig_03" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_02.sh
elif [ "${experiment}" = "fig_08" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_08.sh
elif [ "${experiment}" = "fig_09" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_08.sh
elif [ "${experiment}" = "fig_10" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_08.sh
elif [ "${experiment}" = "fig_11" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_11.sh
elif [ "${experiment}" = "fig_12" ]; then
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_12.sh
else
	echo "Generating all plots!"
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_01.sh
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_02.sh
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_08.sh
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_10.sh
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_11.sh
	${ROOT_DIR}/scripts/parse_data.sh exp_conf/fig_12.sh
fi

