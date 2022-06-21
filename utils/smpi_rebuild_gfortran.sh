#!/bin/bash

_COMPILER_MODULE="${1:-}"
_SMPI_MODULE="${2:-spectrum-mpi}"
_PREFIX="${3:-}"

if [[ -z "${_COMPILER_MODULE}" || -z "${_SMPI_MODULE}" ]]; then
  echo "USAGE: ./$0 COMPILER_MODULE [SMPI_MODULE]"
  echo "   eg: ./$0 \"gcc/7.5.0\" [\"spectrum-mpi/default\"] [PREFIX]"
  exit 1
fi

# Abort on first error
set -e

module purge
module load "${_COMPILER_MODULE}"
if [[ -z "${_PREFIX}" ]]; then
  # Get SMPI dir from module
  module load "${_SMPI_MODULE}"
  PREFIX="${OLCF_SPECTRUM_MPI_ROOT}"
  # PREFIX="/sw/ascent/spack-envs/base/opt/linux-rhel8-ppc64le/gcc-7.5.0/spectrum-mpi-10.4.0.3-20210112-puowkoejepfjtm22sk2dxb6eeup5w447"
  module unload spectrum-mpi
else
  PREFIX="${_PREFIX}"
  echo "Using manually specified prefix: '${PREFIX}'"
fi

# Locate compilers and set SMPI fortran module rebuild parameters
case "${_COMPILER_MODULE%%/*}" in
  gcc)
    _SUFFIX="gfortran"
    OMPI_FC="$(which gfortran)"
    OMPI_CC="$(which gcc)"
    # FORTSUPPORT_PIC_FFLAGS="-fPIC"
    # FORTSUPPORT_PIC_CFLAGS="-fPIC"
    # FORTSUPPORT_PIC_LDFLAGS="-fPIC -shared"
    # FORTSUPPORT_SUFFIX="custom"
    # FORTSUPPORT_OPT="-O3"
    ;;
  nvhpc)
    _SUFFIX="PGI"
    OMPI_FC="$(which nvfortran)"
    OMPI_CC="$(which nvc)"
    # FORTSUPPORT_PIC_FFLAGS="-fPIC"
    # FORTSUPPORT_PIC_CFLAGS="-fPIC"
    # FORTSUPPORT_PIC_LDFLAGS="-fPIC -shared"
    # FORTSUPPORT_SUFFIX="custom"
    # FORTSUPPORT_OPT="-O3"
    ;;
  *)
    echo "ERROR: Cannot identify compiler binaries for ${_COMPILER_MODULE}"
    echo "       Only 'gcc/*' or 'nvhpc/*' are supported"
    exit 1
    ;;
esac

export MPI_ROOT="${PREFIX}"
[ -x $OMPI_FC ] && export OMPI_FC || (echo "ERROR: '$OMPI_FC' not executable!" && exit 1)
[ -x $OMPI_CC ] && export OMPI_CC || (echo "ERROR: '$OMPI_CC' not executable!" && exit 1)
[ -n "${FORTSUPPORT_PIC_FFLAGS:-}" ]  && export FORTSUPPORT_PIC_FFLAGS
[ -n "${FORTSUPPORT_PIC_CFLAGS:-}" ]  && export FORTSUPPORT_PIC_CFLAGS
[ -n "${FORTSUPPORT_PIC_LDFLAGS:-}" ] && export FORTSUPPORT_PIC_LDFLAGS
[ -n "${FORTSUPPORT_SUFFIX:-}" ]      && export FORTSUPPORT_SUFFIX
[ -n "${FORTSUPPORT_OPT:-}" ]         && export FORTSUPPORT_OPT


################
# Backup original pre-compiled fortran modules
cd "${PREFIX}/lib"
if [ ! -d "fortsupport_${_SUFFIX}_stock" ]; then
  if [ -d "fortsupport_${_SUFFIX}" ]; then
    mv "fortsupport_${_SUFFIX}" "fortsupport_${_SUFFIX}_stock"
  fi
  mkdir "${PREFIX}/lib/fortsupport_${_SUFFIX}"
fi
################

################
# Rebuild the fortran modules
cd "${PREFIX}/lib/fortsupport_rebuild"
./build.sh
################

################
# Install new fortran headers in their default locations
cd "${PREFIX}/lib/fortsupport_rebuild"
[ ! -f "${PREFIX}/include/mpif-sizeof-stock.h" ] \
  && mv "${PREFIX}/include/mpif-sizeof.h" "${PREFIX}/include/mpif-sizeof-stock.h"
cp -u ./mpif-sizeof.h "${PREFIX}/include/mpif-sizeof.h"
################

################
# Install new fortran modules in their default locations
cd "${PREFIX}/lib/fortsupport_rebuild"
cp -u *.mod  "${PREFIX}/lib/fortsupport_${_SUFFIX}/."
# cp mpi.mod                          "${PREFIX}/lib/fortsupport_{_SUFFIX}/."
# cp mpi_f08.mod                      "${PREFIX}/lib/fortsupport_{_SUFFIX}/."
# cp mpi_f08_types.mod                "${PREFIX}/lib/fortsupport_{_SUFFIX}/."
# cp mpi_f08_callbacks.mod            "${PREFIX}/lib/fortsupport_{_SUFFIX}/."
# cp mpi_f08_interfaces.mod           "${PREFIX}/lib/fortsupport_{_SUFFIX}/."
# cp mpi_f08_interfaces_callbacks.mod "${PREFIX}/lib/fortsupport_{_SUFFIX}/."
# cp pmpi_f08_interfaces.mod          "${PREFIX}/lib/fortsupport_{_SUFFIX}/."
chmod a+x "${PREFIX}/lib/fortsupport_${_SUFFIX}"/*
################

################
# Install new fortran libraries in their default locations
cd "${PREFIX}/lib/fortsupport_rebuild"
cp -u "libmpi_ibm_usempi_ignore_tkr_custom.so"        "${PREFIX}/lib/."
cp -u "libmpi_ibm_usempi_ignore_tkr_custom_archive.a" "${PREFIX}/lib/."
cp -u "libmpi_ibm_usempif08_custom.so"                "${PREFIX}/lib/."
cp -u "libmpi_ibm_usempif08_custom_archive.a"         "${PREFIX}/lib/."

# Backup existing fortran libraries/archives and update symlinks to new libs
cd "${PREFIX}/lib"
[ ! -f  "libmpi_ibm_usempif08_${_SUFFIX}_stock.so" ] \
  && mv "libmpi_ibm_usempif08_${_SUFFIX}.so" \
        "libmpi_ibm_usempif08_${_SUFFIX}_stock.so"
ln -fs   "libmpi_ibm_usempif08_custom.so" "libmpi_ibm_usempif08_${_SUFFIX}.so"

[ ! -f  "libmpi_ibm_usempi_ignore_tkr_${_SUFFIX}_stock.so" ] \
  && mv "libmpi_ibm_usempi_ignore_tkr_${_SUFFIX}.so" \
        "libmpi_ibm_usempi_ignore_tkr_${_SUFFIX}_stock.so"
ln -fs  "libmpi_ibm_usempi_ignore_tkr_custom.so" "libmpi_ibm_usempi_ignore_tkr_${_SUFFIX}.so"
################
