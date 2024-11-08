#!/bin/bash

source env.sh

experiment_batch=$1


if [ "${experiment_batch}" = "fig_01" ]; then
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_01.sh
elif [ "${experiment_batch}" = "fig_02" ]; then
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_02.sh
elif [ "${experiment_batch}" = "fig_03" ]; then
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_03.sh
elif [ "${experiment_batch}" = "fig_04" ]; then
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_03.sh
elif [ "${experiment_batch}" = "fig_08" ]; then
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_08.sh
elif [ "${experiment_batch}" = "fig_09" ]; then
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_08.sh
elif [ "${experiment_batch}" = "fig_10" ]; then
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_08.sh
elif [ "${experiment_batch}" = "fig_11" ]; then
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_11.sh
elif [ "${experiment_batch}" = "fig_12" ]; then
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_12.sh
elif [ "${experiment_batch}" = "fig_13" ]; then
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_13.sh
elif [ "${experiemnt}" == "AE"]; then
	echo "Running AE experiment_batchs..."
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_08.sh
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_11.sh
elif [ "${experiments}" == "all" ]; then
	echo "Running all experiments..."
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_01.sh
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_02.sh
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_03.sh
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_08.sh
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_11.sh
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_12.sh
	${ROOT_DIR}/scripts/submit_experiment_batch.sh ${ROOT_DIR}/exp_conf/fig_13.sh
else 
	echo "There is no option avaiable for ${experiments}." 
fi

