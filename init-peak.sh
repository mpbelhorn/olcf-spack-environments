#!/bin/bash

# This script must be sourced.
([[ -n $ZSH_EVAL_CONTEXT && $ZSH_EVAL_CONTEXT =~ :file$ ]] || 
 [[ -n $KSH_VERSION && $(cd "$(dirname -- "$0")" &&
       printf '%s' "${PWD%/}/")$(basename -- "$0") != "${.sh.file}" ]] || 
  [[ -n $BASH_VERSION ]] && (return 0 2>/dev/null)) && sourced=1 || sourced=0


[ ${sourced} -eq 0 ] \
  && echo "ERROR: This script must be sourced!" \
  && echo "usage: '. ./init-peak.sh'" \
  && exit 1

[ ! -f "./hosts/peak/spack/share/spack/setup-env.sh" ] \
  && echo "ERROR: This script must be sourced from the root stack manager directory!" \
  && return 1

# Do nothing if a spack instance is already initialized.
[[ -n "${SPACK_ROOT:-}" ]] \
  && echo "Spack is already initialized!" \
  && echo "  '${SPACK_ROOT}'" \
  && echo "Please restart shell to change configuration." \
  && return 1

_spack_host="$(hostname --long \
               | sed -e 's/\.\(olcf\|ccs\)\..*//' \
                     -e 's/[-]\?\(login\|ext\|batch\)[^\.]*[\.]\?//' \
                     -e 's/[-0-9]*$//')"

# TODO : Setup spack instance in host path if it doesn't exist
#  - clone spack
#  - sync hooks
#  - sync configs/environments

ENV_MODROOT="/sw/.b2/envs/peak/base/modules/lmod"

# Copy git tracked modules to module root.
mkdir -p "${ENV_MODROOT}"
cp -dRu --preserve=mode,timestamps "./hosts/${_spack_host}/share/lmod/modulefiles/static/site" "${ENV_MODROOT}/."

# TODO: correct symlinks currently tracked in git repo. This really ought to be an
# OLCF spack extension.
if false; then
for f in $(find "${ENV_MODROOT}/site/Core" \
    -type f \
    \( -ipath "*/Core/gcc/*" \
       -o -ipath "*/Core/xl/*" \
       -o -ipath "*/Core/llvm/*" \) \
    -a ! -iname ".*.lua" \
    -a ! -iname "*-debug.lua"); do
  echo $f | sed -e "s|^${ENV_MODROOT}/site/Core/||" -e 's|.lua$||'
done
fi


# Setup alternate module environment
module purge
export MODULEPATH="${ENV_MODROOT}/spack/linux-rhel7-ppc64le/Core:$ENV_MODROOT/site/Core:/sw/peak/modulefiles/core"
module load python/3.7.0-anaconda3-5.3.0
export PYTHONDONTWRITEBYTECODE=1
source ./hosts/${_spack_host}/spack/share/spack/setup-env.sh
echo "Spack initialized for ${_spack_host:-Unknown host} at ${SPACK_ROOT}"
spack env activate -d /sw/.testing/belhorn/spack/facility-spack/hosts/peak/envs/base
