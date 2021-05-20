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
  'hip@${ROCM_VERSION}%gcc@7.5.0' \
  'hip-rocclr@${ROCM_VERSION}%gcc@7.5.0' \
  'comgr@${ROCM_VERSION}%gcc@7.5.0' \
  'rocm-cmake@${ROCM_VERSION}%gcc@7.5.0' \
  'rocm-openmp-extras@${ROCM_VERSION}%gcc@7.5.0' \
  'rocm-device-libs@${ROCM_VERSION}%gcc@7.5.0' \
  'hsa-rocr-dev@${ROCM_VERSION}%gcc@7.5.0' \
  'hsakmt-roct@${ROCM_VERSION}%gcc@7.5.0' \
  'rocminfo@${ROCM_VERSION}%gcc@7.5.0' \
  'rccl@${ROCM_VERSION}%gcc@7.5.0' \
  'hipblas@${ROCM_VERSION}%gcc@7.5.0' \
  'hipfft@${ROCM_VERSION}%gcc@7.5.0' \
  'hipcub@${ROCM_VERSION}%gcc@7.5.0' \
  'hipsparse@${ROCM_VERSION}%gcc@7.5.0' \
  'hipfort@${ROCM_VERSION}%gcc@7.5.0' \
  'rocm-clang-ocl@${ROCM_VERSION}%gcc@7.5.0' \
  'rocm-opencl-runtime@${ROCM_VERSION}%gcc@7.5.0' \
  'rocblas@${ROCM_VERSION}%gcc@7.5.0' \
  'rocfft@${ROCM_VERSION}%gcc@7.5.0' \
  'rocrand@${ROCM_VERSION}%gcc@7.5.0' \
  'rocthrust@${ROCM_VERSION}%gcc@7.5.0' \
  'rocsolver@${ROCM_VERSION}%gcc@7.5.0' \
  'rocsparse@${ROCM_VERSION}%gcc@7.5.0' \
  'rocprim@${ROCM_VERSION}%gcc@7.5.0' \
  'rocprofiler-dev@${ROCM_VERSION}%gcc@7.5.0' \
  'rocm-smi-lib@${ROCM_VERSION}%gcc@7.5.0' \
  'miopen-hip@${ROCM_VERSION}%gcc@7.5.0' \
  'rocalution@${ROCM_VERSION}%gcc@7.5.0' \
  'rocm-gdb@${ROCM_VERSION}%gcc@7.5.0'"

VIEW_SPECS_ROUND_TWO="\
  'llvm-amdgpu@${ROCM_VERSION}%gcc@7.5.0'"

## Excluded or missing specs
  # 'hipify-clang@${ROCM_VERSION}%gcc@7.5.0' \
  # 'rocm-opencl@${ROCM_VERSION}%gcc@7.5.0' \
  # 'rocm-smi@${ROCM_VERSION}%gcc@7.5.0' \

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
