#!/bin/bash

source ./env.sh

HOME=${ROOT_DIR}

BENCHSUITE=$1 
BIN=$2
DESCR_TAG=$3

mkdir -p ${DUMP_DIR}

echo "#!/bin/bash

#SBATCH -o ${DUMP_DIR}/${DESCR_TAG}_run.out 
#SBATCH -J chmpS_${DESCR_TAG}_run
#SBATCH -A bsc18
#SBATCH --qos=gp_bsccs
#SBATCH --time=00:10:00

source ${HOME}/scripts/benchmarks.sh
export TRACES_DIR="${TRACES_DIR}/\${TRACES_PATH}"

for trace in \${TRACES}; do

	export suffix=.champsimtrace.xz 
  export bench=\${trace%$suffix}


	echo \${TRACES_PATH}

	export PTP_EXTRA_STATS_FILE=${HOME}/dump/\${bench}_${DESCR_TAG}_access_rate.csv
	export RECALL_DIST_FILENAME_PREFIX=${HOME}/dump/\${bench}_${DESCR_TAG}_recall_dist
	export INSTR_PAGE_DIST_FILENAME=${TRACE_EXT_DIR}/\${bench}${INSTR_PAGE_DIST_FILENAME_SUFFIX}.pdst
	export DATA_PAGE_DIST_FILENAME=${TRACE_EXT_DIR}/\${bench}${DATA_PAGE_DIST_FILENAME_SUFFIX}.pdst
	export PAGE_ADDRESS_STATS_FILENAME_PREFIX=${HOME}/dump/\${bench}_${DESCR_TAG}_page_access_stats

	${CHAMPSIM_DIR}/bin/${BIN} 	--warmup_instructions ${SIM_WARMUP_INSTR} \
															--simulation_instructions ${SIM_RUN_INSTR} \
															\${TRACES_DIR}/\${trace} > ${DUMP_DIR}/\${bench}${DESCR_TAG}_run.out 
done
" >	simr_${DESCR_TAG}_job.run
		sbatch simr_${DESCR_TAG}_job.run
		#chmod +x simt_${bench}_job.run
		#./simt_${bench}_job.run
		#rm simr_${DESCR_TAG}_job.run

