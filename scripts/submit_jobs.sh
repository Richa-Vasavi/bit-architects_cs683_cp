#!/bin/bash

HOME=`pwd`

BENCHSUITE=$1 
BIN=$2
DESCR_TAG=$3

echo $DUMP_DIR
mkdir -p ${DUMP_DIR}

source ${HOME}/scripts/benchmarks.sh
export TRACES_DIR="${TRACES_DIR}/${TRACES_PATH}"

for trace in $TRACES; do

	export suffix=.champsimtrace.xz 
  export bench=${trace%$suffix}

	echo "${bench}${DESCR_TAG}"

echo "#!/bin/bash
#SBATCH -N 1
#SBATCH -o ${DUMP_DIR}/${bench}${DESCR_TAG}_run.out 
#SBATCH -J chmpS_${bench}${DESCR_TAG}_run
#SBATCH -q all 
##SBATCH -q large
#SBATCH --time=04:00:00

export PTP_EXTRA_STATS_FILE=${HOME}/dump/${bench}${DESCR_TAG}_access_rate.csv
export RECALL_DIST_FILENAME_PREFIX=${HOME}/dump/${bench}${DESCR_TAG}_recall_dist
export INSTR_PAGE_DIST_FILENAME=${TRACE_EXT_DIR}/${bench}${INSTR_PAGE_DIST_FILENAME_SUFFIX}.pdst
export DATA_PAGE_DIST_FILENAME=${TRACE_EXT_DIR}/${bench}${DATA_PAGE_DIST_FILENAME_SUFFIX}.pdst
export PAGE_ADDRESS_STATS_FILENAME_PREFIX=${HOME}/dump/${bench}${DESCR_TAG}_page_access_stats

gdb -batch -ex "r" -ex "bt" -ex "q" --args \
	${ROOT_DIR}/bin/${BIN} 	--warmup_instructions ${SIM_WARMUP_INSTR} \
								--simulation_instructions ${SIM_RUN_INSTR} \
								${TRACES_DIR}/$trace

" >	simr_${bench}_job.run
		sbatch simr_${bench}_job.run
		#chmod +x simt_${bench}_job.run
		#./simt_${bench}_job.run
		rm simr_${bench}_job.run
done

