#!/bin/bash

## reentrant installation script for "Hango-Gateway"

work_dir=$(cd $(dirname $0); pwd)

# import common functions (log)
source "${work_dir}"/common/common.sh

helm_version="v0.0.0"
HANGO_NAMESPACE="hango-system"
MESH_OPERATOR_NAMESPACE="mesh-operator"

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

function prepare_for_istioctl() {
    if [ ! -f "${work_dir}"/istioctl/istioctl ]; then
        log "\"istioctl\" cmd is missing, please download it first."
        return 1
    else
        chmod +x "${work_dir}"/istioctl/istioctl
        return 0
    fi
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

function install_istiod() {
    # block for installing
    "${work_dir}"/istioctl/istioctl install -y -f "${work_dir}"/istio/istiod.yaml
}

function install_gateway_proxy() {
    "${work_dir}"/istioctl/istioctl install -y -f "${work_dir}"/istio/proxy.yaml
}

function init_for_namespaces() {
    kubectl create ns "${HANGO_NAMESPACE}"
    kubectl create ns "${MESH_OPERATOR_NAMESPACE}"
}

function install_istio_operator() {
    "${work_dir}"/istioctl/istioctl operator init --watchedNamespaces="${HANGO_NAMESPACE}"
    if [[ $? -ne 0 ]]; then
        log "Istio-Operator init failed, please check manually."
        return 1
    fi
}

function init_for_slime() {
    sh "${work_dir}"/slime/init_for_slime.sh "apply"
    if [[ $? -eq 0 ]]; then
        kubectl apply -f "${work_dir}"/slime/hango-plugin.yaml
    else
        log "Init slime fail, please check your network and resources."
    fi
}

# main entry for this shell script
function main() {
    check_kubectl_ready || exit 1
    get_helm_version || exit 1
    prepare_for_istioctl || exit 1
    log "start to init namespaces."
    init_for_namespaces
    log "start to init slime resources."
    init_for_slime
    log "start to init hango control plane components(asynchronously), you are supposed to check their status manually."
    helm_install_for_hango_component
    log "start to init istio-operator, which is specially for istio components installation."
    install_istio_operator || exit 1
    log "start to init istiod."
    install_istiod
    log "start to hango data plane component."
    install_gateway_proxy
    log "install finished!"
}

# start installation process
main