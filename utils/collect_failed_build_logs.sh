#!/bin/bash

_now="$(\date '+%Y%m%d-%H%M')"
_here="$(pwd)"
_stage_dir="/tmp/$USER/spack-stage"
_archive_name="${LMOD_SYSTEM_NAME:-$(hostname --fqdn)}.failed_build_logs.${_now}.tar"
_archive_path="${_stage_dir}/${_archive_name}"

[ ! -d "${_stage_dir}" ] && exit 1

cd "${_stage_dir}"
find . -maxdepth 3 \( -iname "*.log" -o -iname "*.txt" -o -iname "*.yaml" \) -print0 \
  | tar cvf "${_archive_name}" --null --files-from -
cd "${_here}"
[ -f "${_archive_path}" ] && mv "${_archive_path}" .
