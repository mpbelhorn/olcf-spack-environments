ROCM_VERSION="${ROCM_VERSION:-4.1.0}"
SPECS=""
SPECS+=" 'comgr@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hip@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hip-rocclr@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hipblas@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hipcub@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hipfft@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hipfort@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hipify-clang@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hipsparse@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hsa-rocr-dev@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'hsakmt-roct@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'llvm-amdgpu@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'miopen-hip@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rccl@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocalution@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocblas@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocfft@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-clang-ocl@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-cmake@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-device-libs@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-gdb@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-opencl@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-opencl-runtime@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-openmp-extras@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-smi@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocm-smi-lib@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocminfo@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocprim@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocprofiler-dev@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocrand@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocsolver@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocsparse@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'rocthrust@${ROCM_VERSION}%gcc@7.5.0'"
SPECS+=" 'roctracer-dev@${ROCM_VERSION}%gcc@7.5.0'"

SPEC_FORMAT="{/hash:7} {name}@{version}%{compiler}{variants}{arch=architecture}"

spack find --format "${SPEC_FORMAT}" ${SPECS}
unset ROCM_VERSION SPECS SPEC_FORMAT
