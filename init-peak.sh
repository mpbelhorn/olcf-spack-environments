#!/bin/bash

#####################
# Obtain the path to this file.
#   `_THIS`  : path to this file
#   `_THIS_DIR`: path to parent directory of ${_THIS}
# First determine if script is sourced or executed
if [[ "$0" != "${BASH_SOURCE:-}" ]]; then
  # Script is sourced
  _SOURCED=1
  _THIS="$(which $0)"
else
  # Script is executed
  _SOURCED=0
  _THIS="${BASH_SOURCE[0]}"
fi
while [ -h "$_THIS" ]; do
  # resolve $_THIS until the file is no longer a symlink
  _THIS_DIR="$( cd -P "$( dirname "$_THIS" )" >/dev/null && pwd )"

  # if $_THIS was a relative symlink, we need to resolve it relative to the
  # path where the symlink file was located
  _THIS="$(readlink "$_THIS")"
  [[ $_THIS != /* ]] && _THIS="$_THIS_DIR/$_THIS" 
done
_THIS_DIR="$( cd -P "$( dirname "$_THIS" )" >/dev/null && pwd )"
#####################

# This script must be sourced.
[ ${_SOURCED} -eq 0 ] \
  && echo "ERROR: This script must be sourced!" \
  && echo "usage: '. ./init-peak.sh'" \
  && exit 1

# Do nothing if a spack instance is already initialized.
[[ -n "${SPACK_ROOT:-}" ]] \
  && echo "Spack is already initialized!" \
  && echo "  '${SPACK_ROOT}'" \
  && echo "Please restart shell to change configuration." \
  && return 1

_THIS_HOST="$(hostname --long \
             | sed -e 's/\.\(olcf\|ccs\)\..*//' \
                   -e 's/[-]\?\(login\|ext\|batch\)[^\.]*[\.]\?//' \
                   -e 's/[-0-9]*$//')"

[[ "${_THIS_HOST:-XX}" == "XX" ]] \
  && echo "ERROR: Current host '${_THIS_HOST}' could not be identified!" \
  && return 1
[ ! -d "${_THIS_DIR}/hosts/${_THIS_HOST}/envs/base" ] \
  && echo "ERROR: Current host '${_THIS_HOST}' does not have a base environment!" \
  && return 1
_HOST_CONF_DIR="${_THIS_DIR}/hosts/${_THIS_HOST}"

# Copy git-tracked modules to module root.
# FIXME: Need to sync this configuration with the spack environment in use.
ENV_MODROOT="/sw/.b2/envs/peak/base/modules/lmod"
mkdir -p "${ENV_MODROOT}"
cp -dRu --preserve=mode,timestamps "${_HOST_CONF_DIR}/share/lmod/modulefiles/static/site" "${ENV_MODROOT}/."

# Setup alternate module environment
module purge
# FIXME: Need to generalize this across multiple hosts.
export MODULEPATH="${ENV_MODROOT}/spack/linux-rhel7-ppc64le/Core:$ENV_MODROOT/site/Core:/sw/peak/modulefiles/core"

# FIXME: We should use a different python interpretor or a generic one that is
# portable across all hosts.
module load python/3.7.0-anaconda3-5.3.0

export PYTHONDONTWRITEBYTECODE=1
source "${_THIS_DIR}/spack/share/spack/setup-env.sh"
echo "Spack initialized for ${_THIS_HOST:-Unknown host} at ${SPACK_ROOT}"
spack env activate -d "${_HOST_CONF_DIR}/envs/base"
