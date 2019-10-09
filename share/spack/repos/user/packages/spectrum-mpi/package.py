# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SpectrumMpi(Package):
    """IBM MPI implementation from Spectrum MPI."""

    homepage = "http://www-03.ibm.com/systems/spectrum-computing/products/mpi"

    provides('mpi')

    def install(self, spec, prefix):
        raise InstallError('IBM MPI is not installable; it is vendor supplied')

    def setup_dependent_package(self, module, dependent_spec):
        # get library name and directory
        self.spec.mpi_base_dir = self.prefix
        self.spec.mpi_library = join_path(self.prefix.lib, 'libmpi_ibm.so')
        self.spec.mpi_include_path = self.prefix.include
        self.spec.mpi_library_path = self.prefix.lib
        self.spec.mpi_np_flag = '--np'

        # get the compiler names
        if '%xl' in dependent_spec or '%xl_r' in dependent_spec:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpixlc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpixlC')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpixlf')
            self.spec.mpif90 = join_path(self.prefix.bin, 'mpixlf')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpixlf')
        elif '%pgi' in dependent_spec:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpipgicc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpipgic++')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpipgifort')
            self.spec.mpif90 = join_path(self.prefix.bin, 'mpipgifort')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpipgifort')
        else:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpicxx')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpifort')
            self.spec.mpif90 = join_path(self.prefix.bin, 'mpif90')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if '%xl' in dependent_spec or '%xl_r' in dependent_spec:
            spack_env.set('MPICC', join_path(self.prefix.bin, 'mpixlc'))
            spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpixlC'))
            spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpixlf'))
            spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpixlf'))
        elif '%pgi' in dependent_spec:
            spack_env.set('MPICC', join_path(self.prefix.bin, 'mpipgicc'))
            spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpipgic++'))
            spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpipgifort'))
            spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpipgifort'))
        else:
            spack_env.set('MPICC', join_path(self.prefix.bin, 'mpicc'))
            spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpic++'))
            spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
            spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

        spack_env.set('OMPI_CC', spack_cc)
        spack_env.set('OMPI_CXX', spack_cxx)
        spack_env.set('OMPI_FC', spack_fc)
        spack_env.set('OMPI_F77', spack_f77)

        spack_env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)
        spack_env.set('OMPI_DIR', self.prefix)
        spack_env.set('MPI_DIR', self.prefix)


    def setup_environment(self, spack_env, run_env):
        run_env.set('OMPI_DIR', self.prefix)
        run_env.set('MPI_ROOT', self.prefix)
        run_env.set('OPAL_PREFIX', self.prefix)
        run_env.set('OPAL_LIBDIR', self.prefix.lib)

        run_env.set('OMPI_CC', self.compiler.cc)
        run_env.set('OMPI_CXX', self.compiler.cxx)
        run_env.set('OMPI_FC', self.compiler.fc)
