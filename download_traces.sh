
source env.sh

TRACES=$1

mkdir -p ${TRACE_DIR}

if [ ${TRACES} == "qualcomm_srv" ] || [ ${TRACES} == "AE" ]; then
	mkdir -p ${TRACE_DIR}/qualcomm_srv
	zenodo_get -o ${TRACE_DIR}/qualcomm_srv https://doi.org/10.5281/zenodo.14045185
	cd ${TRACE_DIR}
	tar xvf qualcomm_srv.tar 
	rm qualcomm_srv_tar
	tar xvf smt_qualcomm_srv.tar
	rm smt_qualcomm_srv.tar
	cd ${ROOT_DIR}
elif [ ${TRACES} == "spec" ]; then
	mkdir -p ${TRACE_DIR}/spec
	zenodo_get -o ${TRACE_DIR}/spec https://doi.org/10.5281/zenodo.10959704 
	zenodo_get -o ${TRACE_DIR}/spec https://doi.org/10.5281/zenodo.10960003
else
	zenodo_get -o ${TRACE_DIR}/qualcomm_srv https://doi.org/10.5281/zenodo.14045185
	mkdir -p ${TRACE_DIR}/qualcomm_srv
	cd ${TRACE_DIR}
	tar xvf qualcomm_srv.tar 
	rm qualcomm_srv_tar
	tar xvf smt_qualcomm_srv.tar
	rm smt_qualcomm_srv.tar
	cd ${ROOT_DIR}

	mkdir -p ${TRACE_DIR}/spec
	zenodo_get -o ${TRACE_DIR}/spec https://doi.org/10.5281/zenodo.10959704 
	zenodo_get -o ${TRACE_DIR}/spec https://doi.org/10.5281/zenodo.10960003
fi
