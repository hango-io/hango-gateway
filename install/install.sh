#!/bin/bash

## reentrant installation script for "Hango-Gateway"

work_dir=$(cd $(dirname $0); pwd)

# import common functions (log)
source "${work_dir}"/common/common.sh

helm_version="v0.0.0"
HANGO_NAMESPACE="hango-system"
MESH_OPERATOR_NAMESPACE="mesh-operator"
# install shell home
INIT_SHELL_DIR=$(cd "$(dirname "$0")";pwd)
# crd home
CRD_DIR=${INIT_SHELL_DIR}/crds

function check_kubectl_ready() {
    kubectl version >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "Your k8s and kubectl are both ready? please check manually."
        return 1
    fi
}

function get_helm_version() {
    helm >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        log "Please install helm first."
        return 1
    fi
    helm_version=$(helm version | awk -F "Version:" '{print $2}' | awk -F '"' '{print $2}')
}

# Check whether the version of helm is later than V3
function helm_version_judge() {
    version_prefix=$(echo "${helm_version}" | awk -F "." '{print $1}')
    if [[ "${version_prefix}" = "v3" ]]; then
        return 0
    elif [[ "${version_prefix}" = "v2" ]]; then
        return 1
    else
        return 2
    fi
}

# prepare crds
function prepare_for_crds() {
    for crd in `ls "${CRD_DIR}"`; do
        kubectl apply -f ${CRD_DIR}/${crd}
        if [ "$?" -ne 0 ]; then
            echo "kubectl apply crd failed, crd_name: ${CRD_DIR}/${crd}"
            return 1
        fi
    done
}

function helm_install_for_hango_component() {
    helm_version_judge
    if [[ $? -eq 0 ]]; then
        # 3.x version above
        helm install --namespace "${HANGO_NAMESPACE}" hango-gateway "${work_dir}"/helm/hango-gateway/ &
    elif [[ $? -eq 1 ]]; then
        # 2.x version above
        helm install --namespace "${HANGO_NAMESPACE}" --name hango-gateway "${work_dir}"/helm/hango-gateway/ &
    else
        log "Your helm version is too old, please update to 3.x version above."
        exit 1
    fi
}

function verify_hango_install() {
    while true
    do
       sleep 10s
       pod_number=`kubectl -n $HANGO_NAMESPACE get pods | grep Running | wc -l`
       if [[ $pod_number -ge 7 ]]; then
          echo "hango pod running"
          break
       fi
    done    
}

function init_for_namespaces() {
    kubectl create ns "${HANGO_NAMESPACE}"
}


# main entry for this shell script
function main() {
    check_kubectl_ready || exit 1
    get_helm_version || exit 1
    prepare_for_crds || exit 1
    log "start to init namespaces."
    init_for_namespaces
    log "start to init hango components(asynchronously), you are supposed to check their status manually."
    helm_install_for_hango_component
    log "install finished!"
    log "start to verify hango install"
    verify_hango_install
    log "hango verfied ok"
    "${work_dir}"/init-hango/init.sh
}

# start installation process
main
