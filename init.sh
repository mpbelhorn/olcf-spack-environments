#!/bin/bash

# This script must be sourced.
([[ -n $ZSH_EVAL_CONTEXT && $ZSH_EVAL_CONTEXT =~ :file$ ]] || 
 [[ -n $KSH_VERSION && $(cd "$(dirname -- "$0")" &&
       printf '%s' "${PWD%/}/")$(basename -- "$0") != "${.sh.file}" ]] || 
  [[ -n $BASH_VERSION ]] && (return 0 2>/dev/null)) && sourced=1 || sourced=0


[ ${sourced} -eq 0 ] \
  && echo "ERROR: This script must be sourced!" \
  && echo "usage: '. ./init.sh'" \
  && exit 1

[ ! -f "./spack/share/spack/setup-env.sh" ] \
  && echo "ERROR: This script must be sourced from the root stack manager directory!" \
  && return 1

# Do nothing if a spack instance is already initialized.
[[ -n "${SPACK_ROOT:-}" ]] \
  && echo "Spack is already initialized!" \
  && echo "  '${SPACK_ROOT}'" \
  && echo "Please restart shell to change configuration." \
  && return 1

if [ -n "${ZSH_VERSION:-}" ]; then
    emulate -L sh
fi

_spack_host="$(hostname --long \
               | sed -e 's/\.\(olcf\|ccs\)\..*//' \
                     -e 's/[-]\?\(login\|ext\|batch\)[^\.]*[\.]\?//' \
                     -e 's/[-0-9]*$//')"

# TODO : Setup spack instance in host path if it doesn't exist
#  - clone spack
#  - sync hooks
#  - sync configs/environments
# FIXME : Ensure a python3 interpereter is available for all systems.
[ -n "${LMOD_SYSTEM_NAME}" ] && module purge && module load python
export PYTHONDONTWRITEBYTECODE=1
source ./hosts/${_spack_host}/spack/share/spack/setup-env.sh
echo "Spack initialized for ${_spack_host:-Unknown host} at ${SPACK_ROOT}"
