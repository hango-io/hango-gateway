#!/bin/bash

## uninstall script for "Hango-Gateway"

work_dir=$(cd $(dirname $0); pwd)

# import common functions (log)
source "${work_dir}"/common/common.sh

LOG_PREFIX="hango_uninstall"
DATA_FORMAT="+%H:%M:%S"
MESH_OPERATOR_NAMESPACE="mesh-operator"
ISTIO_OPERATOR_NAMESPACE="istio-operator"
HANGO_SYSTEM_NAMESPACE="hango-system"

# uninstall istio components
log "start to uninstall hango gateway."
"${work_dir}"/istioctl/istioctl x uninstall -y --purge

log "start to uninstall hango components."
helm delete hango-gateway -n hango-system
helm delete hango-plugin -n hango-system

kubectl delete -f "${work_dir}"/slime/hango-plugin.yaml

log "start to uninstall slime components."
sh "${work_dir}"/slime/init_for_slime.sh "delete"

log "start to uninstall namespace[${ISTIO_OPERATOR_NAMESPACE}]"
kubectl get ns "${ISTIO_OPERATOR_NAMESPACE}">/dev/null 2>&1
if [[ $? -eq 0 ]]; then
    kubectl delete ns "${ISTIO_OPERATOR_NAMESPACE}"
fi

log "start to uninstall namespace[${MESH_OPERATOR_NAMESPACE}]"
kubectl get ns "${MESH_OPERATOR_NAMESPACE}">/dev/null 2>&1
if [[ $? -eq 0 ]]; then
    kubectl delete ns "${MESH_OPERATOR_NAMESPACE}"
fi

log "start to uninstall namespace[${HANGO_SYSTEM_NAMESPACE}]"
kubectl get ns "${HANGO_SYSTEM_NAMESPACE}">/dev/null 2>&1
if [[ $? -eq 0 ]]; then
    kubectl delete ns "${HANGO_SYSTEM_NAMESPACE}"
fi

log "uninstall finished!"