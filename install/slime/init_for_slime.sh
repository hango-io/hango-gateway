#!/bin/bash

work_dir=$(cd $(dirname $0); pwd)

# import common functions (log)
source "${work_dir}"/../common/common.sh

LOG_PREFIX="slime"
DATA_FORMAT="+%H:%M:%S"
operation=$1
# timeout limit for ping (second)
time_out=5
# try count for ping
try_count=1
# github url
github_url="https://raw.githubusercontent.com"

if [[ "${operation}" = "apply" || "${operation}" = "create" || "${operation}" = "delete" ]]; then
    # TODO this url is missing, search for another way to ensure url is ok
    ping -c "${try_count}" -w "${time_out}" "${github_url}" >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        log "${github_url} is unreachable, please check manually."
    fi
    kubectl "${operation}" -f "${github_url}/slime-io/slime/v0.1/install/init/crds.yaml"
    kubectl "${operation}" -f "${github_url}/slime-io/slime/v0.1/install/init/slime-boot-install.yaml"
else
    log "illegal operation for kubectl to deal resources"
    exit 1
fi