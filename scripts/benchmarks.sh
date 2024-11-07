
TRACE_DIR="/scratch/nas/3/dchasapi/champsim_traces"

source ./scripts/spec_cpu_workloads.sh
source ./scripts/qualcomm_srv_workloads.sh

if [ "${BENCHSUITE}" == "qualcomm_srv_ap"  ]; then
			TRACES="${QUALCOMM_SRV_AP}"
			TRACES_PATH="${QUALCOMM_SRV_AP_DIR}"
elif [ "${BENCHSUITE}" == "selected_qualcomm_srv_ap"  ]; then
			TRACES="${SELECTED_QUALCOMM_SRV_AP}"
			TRACES_PATH="${QUALCOMM_SRV_AP_DIR}"
elif [ "${BENCHSUITE}" == "smt_qualcomm_srv_ap"  ]; then
			TRACES="${SMT_QUALCOMM_SRV_AP}"
			TRACES_PATH="${QUALCOMM_SRV_AP_DIR}"
elif [ "${BENCHSUITE}" == "spec" ]; then
			TRACES="${SPEC_CPU_2006} ${SPEC_CPU_2017}"
			TRACES_PATH="${SPEC_CPU_DIR}"
else
			TRACES=smt_srv12_ap_srv99_ap_1024i.champsimtrace.xz
			TRACES_PATH="${QUALCOMM_SRV_AP_DIR}"
fi

SIMPOINTS=''
for trace in $TRACES; do	
	export suffix=.champsimtrace.xz 
	export bench=${trace%$suffix}
	SIMPOINTS="$SIMPOINTS $bench"
done

BENCHMARKS=''
for simpoint in $SIMPOINTS; do
	export suffix=-*
	export bench=${simpoint%$suffix}
	BENCHMARKS="${BENCHMARKS} ${bench}"
done
BENCHMARKS=$(echo "${BENCHMARKS}" | xargs -n1 | sort -u | xargs)

