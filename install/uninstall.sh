#!/bin/bash

## uninstall script for "Hango-Gateway"

work_dir=$(cd $(dirname $0); pwd)

# import common functions (log)
source "${work_dir}"/common/common.sh

LOG_PREFIX="hango_uninstall"
DATA_FORMAT="+%H:%M:%S"
HANGO_SYSTEM_NAMESPACE="hango-system"


log "start to uninstall hango components."
helm status hango-gateway -n hango-system >/dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "helm component hango-gateway not exists, no need to delete"
else
    helm delete hango-gateway -n hango-system
fi

log "start to uninstall namespace[${HANGO_SYSTEM_NAMESPACE}]"
kubectl get ns "${HANGO_SYSTEM_NAMESPACE}" >/dev/null 2>&1
if [[ $? -eq 0 ]]; then
    kubectl delete ns "${HANGO_SYSTEM_NAMESPACE}"
fi

log "start to delete k8s crd of hango"
kubectl get crd | grep -E "slime|istio" >/dev/null 2>&1
if [[ $? -eq 0 ]]; then
    kubectl get crd | grep -E "slime|istio" | awk '{print $1}' | xargs kubectl delete crd
fi

log "uninstall finished!"