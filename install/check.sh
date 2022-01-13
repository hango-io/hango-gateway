#!/bin/bash

## container status check script for "Hango-Gateway"

work_dir=$(cd $(dirname $0); pwd)

# import common functions (log)
source "${work_dir}"/common/common.sh

LOG_PREFIX="install-check"
DATA_FORMAT="+%H:%M:%S"
MESH_OPERATOR_NAMESPACE="mesh-operator"
ISTIO_OPERATOR_NAMESPACE="istio-operator"
HANGO_SYSTEM_NAMESPACE="hango-system"

echo -e "\nPlease wait for all pods status running and ready. If it persists for long time, manually check it.\n"

log "\n========= pods in namespace[\033[44;37;25m${MESH_OPERATOR_NAMESPACE}\033[0m] show below ========="
kubectl -n "${MESH_OPERATOR_NAMESPACE}" get pods
echo ""

log "\n========= pods in namespace[\033[44;37;25m${ISTIO_OPERATOR_NAMESPACE}\033[0m] show below ========="
kubectl -n "${ISTIO_OPERATOR_NAMESPACE}" get pods
echo ""

log "\n========= pods in namespace[\033[44;37;25m${HANGO_SYSTEM_NAMESPACE}\033[0m] show below ========="
kubectl -n "${HANGO_SYSTEM_NAMESPACE}" get pods