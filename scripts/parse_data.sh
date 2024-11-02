
CONFIG_FILE=$1
source $CONFIG_FILE


for BENCHSUITE in ${BENCHSUITES}; do

	for TAG in ${CONFIGURATION_TAGS}; do	
		TAG="_${TAG}"

		source ${ROOT_DIR}/scripts/benchmarks.sh

		if [[ "${BENCHSUITE}" == *"spec"* ]]; then
			BENCHNAMES=${BENCHMARKS}
			BENCHMARKS=${SIMPOINTS}
			SIMPOINTS=${SIMPOINTS}
		else
			BENCHNAMES=""
			BENCHMARKS=${SIMPOINTS}
			SIMPOINTS=""
		fi
		

		mkdir -p ${ROOT_DIR}/stats

		echo "Preparing ${BENCHSUITE}${TAG}..."

		if [ "${GENERATE_STATS}" == "True" ]; then 
			echo "Parsing raw ChampSim data..."
			for bench in ${BENCHMARKS}; do
				status=`python3 ${ROOT_DIR}/scripts/convert_champsim2csv.py --input-file ${ROOT_DIR}/dump/${bench}${TAG}_run.out \
																																			--output ${ROOT_DIR}/stats/${bench}${TAG}.csv`
				if [[ ${status} ]]; then
					echo "Failed parsing ${bench}"
					BENCHMARKS=`echo ${BENCHMARKS} | sed "s/${bench}\b//g"`
					echo ${status}
				fi

			done

			# Apply weights in case benchmarks use simpoints 
			if [[ "${BENCHNAMES}" ]]; then
				echo "Apply simpoint weights..."

				for bench in ${BENCHNAMES}; do
					data_files=''
					for simpoint in ${SIMPOINTS}; do
						if [[ "${simpoint}" == *"${bench}"* ]]; then 
							data_files="${data_files} ./stats/${simpoint}${TAG}.csv"
						fi
					done
						
					python3 ./scripts/apply_weights.py	--input-files $data_files \
																							--simpoints-file ./weights/${bench}/simpoints.out \
																							--weights-file ./weights/${bench}/weights.out \
																							--output-file ./stats/${bench}${TAG}.csv 
				done
				BENCHMARKS=${BENCHNAMES}
			fi


			echo "Merging data into one file..."
			files=''
			for bench in $BENCHMARKS; do
				elems=$(wc -l ${ROOT_DIR}/stats/${bench}${TAG}.csv | cut -d ' ' -f 1)
				if [ "$elems" != "43" ]; then
					echo ${ROOT_DIR}/stats/${bench}${TAG}.csv
				fi 
				
				files="${files} ${ROOT_DIR}/stats/${bench}${TAG}.csv"
			done

			python3 ${ROOT_DIR}/scripts/merge_champsim_data.py	--input-files ${files} \
																													--benchmarks ${BENCHMARKS} \
																													--output-file=${ROOT_DIR}/stats/${BENCHSUITE}${TAG}.csv
		fi


		if [ "${GENERATE_EXTRA_STATS}" == "True" ]; then

			echo "Processing page access stats data..."
			for bench in ${BENCHMARKS}; do
				python3 ${ROOT_DIR}/scripts/process_page_access_stats.py \
										--input-file ${ROOT_DIR}/dump/${bench}${TAG}_page_access_stats \
										--output-file ${ROOT_DIR}/stats/${bench}${TAG}_page_access_stats.csv
			done

			echo "Merging page access stats into one file..."
			files=''
			for bench in $BENCHMARKS; do
				files="${files} ${ROOT_DIR}/stats/${bench}${TAG}_page_access_stats.csv"
			done
				
			python3 ${ROOT_DIR}/scripts/merge_champsim_data.py	--input-files ${files} \
																													--benchmarks ${BENCHMARKS} \
																													--output-file=${ROOT_DIR}/stats/${BENCHSUITE}${TAG}_page_access_stats.csv

		fi

	done
done

