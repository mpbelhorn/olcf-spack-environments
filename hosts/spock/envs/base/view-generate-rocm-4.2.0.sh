#!/bin/bash

ROCM_VERSION="4.2.0"
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

# Specific specs, when needed are selected from the output of:
# ```
# ROCM_VERSION=4.2.0 . ./find-rocm-specs.sh 
# ```

# View conflicts are resolved in first-come:first-used manner. Conflicting specs
# must be added to the view in multiple rounds
SPECS=""
SPECS+=" 'comgr@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hip@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hip-rocclr@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hipblas@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hipcub@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hipfft@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hipfort@${ROCM_VERSION}%gcc@7.5.0'"
# SPECS+=" 'hipify-clang@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hipsparse@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hsa-rocr-dev@${ROCM_VERSION}%gcc@7.5.0 /7lwijot'"
SPECS+=" 'hsakmt-roct@${ROCM_VERSION}%gcc@7.5.0'"
# SPECS+=" 'llvm-amdgpu@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'miopen-hip@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rccl@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocalution@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocblas@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocfft@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-clang-ocl@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-cmake@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-device-libs@${ROCM_VERSION}%gcc@7.5.0 /fqhh65d'"
SPECS+=" 'rocm-gdb@${ROCM_VERSION}%gcc@7.5.0'"
# SPECS+=" 'rocm-opencl@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-opencl-runtime@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-openmp-extras@${ROCM_VERSION}%gcc@7.5.0'"
# SPECS+=" 'rocm-smi@${ROCM_VERSION}%gcc@7.5.0'" ## Not installed for v4.1.0+
SPECS+=" 'rocm-smi-lib@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocminfo@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocprim@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocprofiler-dev@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocrand@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocsolver@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocsparse@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocthrust@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'roctracer-dev@${ROCM_VERSION}%gcc@7.5.0'"

VIEW_SPECS_ROUND_ONE="${SPECS}"
VIEW_SPECS_ROUND_TWO="'llvm-amdgpu@${ROCM_VERSION}%gcc@7.5.0+openmp'"

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

if [ "$?" -eq 0 ]; then
  spack view \
      --dependencies 'false' \
      --verbose \
      symlink --ignore-conflicts \
              --projection-file "hosts/spock/envs/base/view-rocm-${ROCM_VERSION}.yaml" \
              "${TMP_VIEW_ROOT}" \
              ${VIEW_SPECS_ROUND_TWO}

  if [ "$?" -eq 0 ]; then
    # Handle special cases with spack making empty dirs in the view for relative
    # symlinks under a package's install prefix.
    [ -d "${TMP_VIEW_ROOT}/hsa/include/hsa" ] && rmdir --ignore-fail-on-non-empty "${TMP_VIEW_ROOT}/hsa/include/hsa"
    # FIXME - replace with a tarball or script.
    cp -vRP ${PATCH_LINKS}/bin \
            ${PATCH_LINKS}/include \
            ${PATCH_LINKS}/lib \
            ${PATCH_LINKS}/hsa \
            ${PATCH_LINKS}/oam \
            -t ${TMP_VIEW_ROOT}

    if [ "$?" -eq 0 ]; then
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
    else
      # Failed symlink copy
      echo "Failed to copy out relative symlink tree."
      rm -fr "${TMP_VIEW_ROOT}"
      return 1
    fi
  else
    # Failed second round
    echo "Failed second round of view generation."
    rm -fr "${TMP_VIEW_ROOT}"
    return 1
  fi
else
  # Failed first round
  echo "Failed first round of view generation."
  rm -fr "${TMP_VIEW_ROOT}"
  return 1
fi
