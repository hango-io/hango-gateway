#!/bin/bash

# you can override variables below by yours
LOG_DEST_CONSOLE="console"
LOG_DEST_FILE="file"
DATA_FORMAT="+%Y-%m-%d %H:%M:%S"
LOG_FILE="/root/install_hango.log"
LOG_PREFIX="hango-install"
log_dest="${LOG_DEST_CONSOLE}"

# log for installing
function log() {
    tmp_dest="${log_dest}"
    log_time=$(date "${DATA_FORMAT}")

    # temporary choice for log output destination
    if [ $# -gt 1 ]; then
        if [[ "$1" = "${LOG_DEST_CONSOLE}" ]]; then
            log_dest="${LOG_DEST_CONSOLE}"
        elif [[ "$1" = "${LOG_DEST_FILE}" ]]; then
            log_dest="${LOG_DEST_FILE}"
        fi
    fi

    # output the log by destination
    if [[ "${log_dest}" = "${LOG_DEST_CONSOLE}" ]]; then
        echo -e "[${LOG_PREFIX}][${log_time}]" "$*"
    elif [[ "${log_dest}" = "${LOG_DEST_FILE}" ]]; then
        echo -e "[${LOG_PREFIX}][${log_time}]" "$*" >>"${LOG_FILE}"
    else
        echo "Please choose right destination for log output."
    fi
    # restore with original destination
    log_dest="${tmp_dest}"
}
