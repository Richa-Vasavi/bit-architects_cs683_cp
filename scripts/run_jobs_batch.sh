#!/bin/bash

source ./env.sh

BENCHSUITE=$1 
BIN=$2
DESCR_TAG=$3

mkdir -p ${DUMP_DIR}

source ${ROOT_DIR}/scripts/benchmarks.sh
export TRACES_DIR="${TRACE_DIR}/${TRACES_PATH}"

num_retired_benchmarks=1
if [ -f retired_${BENCHSUITE}${DESCR_TAG}.txt ]; then
	IFS=$'\n' read -d '' -r -a retired_benchmaks < retired_${BENCHSUITE}${DESCR_TAG}.txt
	num_retired_benchmarks=$(wc -l < retired_${BENCHSUITE}${DESCR_TAG}.txt)
fi

iter=0
for trace in $TRACES; do

	skip="False"
	for (( i=0; i < ${num_retired_benchmarks}; i++ )); do
		#echo ${trace}
		#echo ${retired_benchmaks[$i]}
		#echo "=========="
		if [[ "${trace}" == ${retired_benchmaks[$i]} ]]; then
			#echo "match!"
			skip="True"
			break
		fi
	done
	sleep 2
	if [[ ${skip} == "True" ]]; then
		#echo "SKIP BENCHMARK"
		continue
	fi
	sleep 2
	export suffix=.champsimtrace.xz 
  export bench=${trace%$suffix}

	echo "running ${bench}${DESCR_TAG}"


	export PTP_EXTRA_STATS_FILE=${DUMP_DIR}/${bench}${DESCR_TAG}_access_rate.csv
	export RECALL_DIST_FILENAME_PREFIX=${DUMP_DIR}/${bench}${DESCR_TAG}_recall_dist
	export INSTR_PAGE_DIST_FILENAME=${DUMP_DIR}/${bench}${INSTR_PAGE_DIST_FILENAME_SUFFIX}.pdst
	export DATA_PAGE_DIST_FILENAME=${DUMP_DIR}/${bench}${DATA_PAGE_DIST_FILENAME_SUFFIX}.pdst
	export PAGE_ADDRESS_STATS_FILENAME_PREFIX=${DUMP_DIR}/${bench}${DESCR_TAG}_page_access_stats

	${CHAMPSIM_DIR}/bin/${BIN} 	--warmup_instructions ${SIM_WARMUP_INSTR} \
															--simulation_instructions ${SIM_RUN_INSTR} \
															${TRACES_DIR}/${trace} > ${DUMP_DIR}/${bench}${DESCR_TAG}_run.out 

	echo "done running ${bench}${DESCR_TAG}"
	echo ${trace} >> retired_${BENCHSUITE}${DESCR_TAG}.txt 

done

