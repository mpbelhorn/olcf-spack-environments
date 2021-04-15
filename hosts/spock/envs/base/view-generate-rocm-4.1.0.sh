#!/bin/bash

ROCM_VERSION="4.1.0"
VIEW_ROOT="/sw/spock/spack-envs/views/rocm-${ROCM_VERSION}"
# Alternate view for debugging
# VIEW_ROOT="/tmp/belhorn/view_tests/rocm-${ROCM_VERSION}"

######################### 
VIEW_PREFIX="$(dirname ${VIEW_ROOT})"
VIEW_NAME="$(basename ${VIEW_ROOT})"

# FIXME - replace with a tarball or script.
PATCH_LINKS="/sw/spock/spack-envs/views/.rocm_symlinks"


if [[ "$0" == "${BASH_SOURCE:-}" ]]; then
  echo "This script must be sourced"
  exit 1
fi

_PREVIOUS_VIEW="${VIEW_PREFIX:-/tmp/facspack-view-regen}/.${VIEW_NAME}.last"
if [ -e "${_PREVIOUS_VIEW}.tmp" ]; then
  echo "Previous failed update exists. Cancelling."
  return 1
fi

# Exit if facility spack environment management runtime is not setup
if [ -z "${FACSPACK_SPACK_ROOT:-}" ]; then
  echo "Facspack not initialized"
  return 1
elif [ -z "${SPACK_ENV:-}" ]; then
  echo "Not in an active spack environment"
  return 1
elif [[ "${FACSPACK_HOST}" != "spock" ]]; then
  echo "Not running on Spock"
  return 1
fi

# View conflicts are resolved in first-come:first-used manner. Conflicting specs
# must be added to the view in multiple rounds
VIEW_SPECS_ROUND_ONE="\
  'hip@${ROCM_VERSION}' \
  'hip-rocclr@${ROCM_VERSION}' \
  'comgr@${ROCM_VERSION}' \
  'rocm-cmake@${ROCM_VERSION}' \
  'rocm-openmp-extras@${ROCM_VERSION}' \
  'rocm-device-libs@${ROCM_VERSION}' \
  'hsa-rocr-dev@${ROCM_VERSION}' \
  'hsakmt-roct@${ROCM_VERSION}' \
  'rocminfo@${ROCM_VERSION}' \
  'rccl@${ROCM_VERSION}' \
  'hipblas@${ROCM_VERSION}' \
  'hipfft@${ROCM_VERSION}' \
  'hipcub@${ROCM_VERSION}' \
  'hipsparse@${ROCM_VERSION}' \
  'hipfort@${ROCM_VERSION}' \
  'rocm-clang-ocl@${ROCM_VERSION}' \
  'rocm-opencl-runtime@${ROCM_VERSION}' \
  'rocblas@${ROCM_VERSION}' \
  'rocfft@${ROCM_VERSION}' \
  'rocrand@${ROCM_VERSION}' \
  'rocthrust@${ROCM_VERSION}' \
  'rocsolver@${ROCM_VERSION}' \
  'rocsparse@${ROCM_VERSION}' \
  'rocprim@${ROCM_VERSION}' \
  'rocm-smi-lib@${ROCM_VERSION}' \
  'miopen-hip@${ROCM_VERSION}' \
  'rocalution@${ROCM_VERSION}' \
  'rocm-gdb@${ROCM_VERSION}'"

VIEW_SPECS_ROUND_TWO="\
  'llvm-amdgpu@${ROCM_VERSION}'"

## Excluded or missing specs
  # 'hipify-clang@${ROCM_VERSION}' \
  # 'rocm-opencl@${ROCM_VERSION}' \
  # 'rocm-smi@${ROCM_VERSION}' \
  # 'rocprofiler-dev@${ROCM_VERSION}' \

[ ! -d "${VIEW_PREFIX}" ] && mkdir -p "${VIEW_PREFIX}"
TMP_VIEW_ROOT=$(mktemp -d -p ${VIEW_PREFIX} XXXXXX)
[ -d "${TMP_VIEW_ROOT}" ] && chmod go=rx "${TMP_VIEW_ROOT}"
spack view \
    --dependencies 'false' \
    --verbose \
    symlink --ignore-conflicts \
            --projection-file "hosts/spock/envs/base/view-rocm-${ROCM_VERSION}.yaml" \
            "${TMP_VIEW_ROOT}" \
            ${VIEW_SPECS_ROUND_ONE}

spack view \
    --dependencies 'false' \
    --verbose \
    symlink --ignore-conflicts \
            --projection-file "hosts/spock/envs/base/view-rocm-${ROCM_VERSION}.yaml" \
            "${TMP_VIEW_ROOT}" \
            ${VIEW_SPECS_ROUND_TWO}

# FIXME - replace with a tarball or script.
cp -vRP ${PATCH_LINKS}/bin \
        ${PATCH_LINKS}/include \
        ${PATCH_LINKS}/lib \
        ${PATCH_LINKS}/oam \
        -t ${TMP_VIEW_ROOT}

if [ -e "${_PREVIOUS_VIEW}.tmp" ]; then
  rm -fr "${TMP_VIEW_ROOT}"
  echo "ERROR: Previous view backup exists '${_PREVIOUS_VIEW}.tmp'."
  return 1
elif [ -d "${_PREVIOUS_VIEW}" ]; then
  /usr/bin/mv -Tn "${_PREVIOUS_VIEW}" "${_PREVIOUS_VIEW}.tmp"
fi

if [ -e "${_PREVIOUS_VIEW}" ]; then
  echo "ERROR: Previous view still exists '${_PREVIOUS_VIEW}'."
  return 1
elif [ -d "${VIEW_ROOT}" ]; then
  /usr/bin/mv -Tn "${VIEW_ROOT}" "${_PREVIOUS_VIEW}" 
fi

if [ -e "${VIEW_ROOT}" ]; then
  echo "ERROR: Current view still exists '${_PREVIOUS_VIEW}'."
  return 1
elif [ -d "${TMP_VIEW_ROOT}" ]; then
  /usr/bin/mv -Tn "${TMP_VIEW_ROOT}" "${VIEW_ROOT}"
fi

if [ -e "${_PREVIOUS_VIEW}.tmp" ]; then
  # echo "DEBUG: Removing prior view backup '${_PREVIOUS_VIEW}.tmp'"
  /usr/bin/rm -fr "${_PREVIOUS_VIEW}.tmp"
fi

echo "Successfully updated view '${VIEW_ROOT}'."
