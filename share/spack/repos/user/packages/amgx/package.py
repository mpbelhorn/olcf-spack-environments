# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Amgx(CMakePackage):
    """Algebraic Multigrid Solver (AmgX) Library
    
    AmgX is a GPU accelerated core solver library that speeds up computationally
    intense linear solver portion of simulations. The library includes a
    flexible solver composition system that allows a user to easily construct
    complex nested solvers and preconditioners. The library is well suited for
    implicit unstructured methods. The AmgX library offers optimized methods for
    massive parallelism, the flexibility to choose how the solvers are
    constructed, and is accessible through a simple C API that abstracts the
    parallelism and scale across a single or multiple GPUs using user provided
    MPI.
    """

    homepage = "https://developer.nvidia.com/amgx"
    url      = "https://github.com/NVIDIA/AMGX/tarball/89e2ace04d906fc2382d490c5ac762ae7915dbc8"

    # MPB (2017-12-04): NVIDIA's github repo does not currently issue releases
    # nor tag releases in the single master branch for AMGX. When updating
    # versions, see `ReleaseVersion.txt` in the repo for the current version and
    # point the version to the latest commit prior to `ReleaseVersion.txt` being
    # updated. If multiple versions are needed of commits between updates to
    # ReleaseVersion, add an integer to indicate the build is effectively a
    # "nightly" build.
    version('2.0.0.130.2', 'b6ab6ddd4ea922ee1423f9d324775aa9',
            url='https://github.com/NVIDIA/AMGX/tarball/a46b3112bc563592b8d794ba95e57350d282d584')
    version('2.0.0.130.1', '0db4f2962fe7333a39c614b3f2b7a246',
            url='https://github.com/NVIDIA/AMGX/tarball/732338c32e30ad87f9b71244346346f66fc3f735')
    version('2.0.0.130.0', '603b4d8889b316e92e193bddd53267c1',
            url='https://github.com/NVIDIA/AMGX/tarball/89e2ace04d906fc2382d490c5ac762ae7915dbc8')

    variant('mpi', default=False, description='Build with MPI support')
    variant('magma', default=False, description='Build with magma support')
    variant('openmp', default=True, description='Build with OpenMP support')

    depends_on('cuda@7:10.99', when='@:2.0.0.130.2')
    depends_on('cuda@7:9.99', when='@:2.0.0.130.1')
    depends_on('magma', when="+magma")
    depends_on('openblas', when="@2.0.0.130.0+magma")
    depends_on('mpi', when='+mpi')

    conflicts('%gcc@:4.8.2', when='%gcc')
    conflicts('%pgi', when='+openmp')
    conflicts('%xl', when='+openmp')
    conflicts('%xl_r', when='+openmp')

    patch('v2_cuda9.patch', when='@2.0.0.130.0')

    def cmake_args(self):
        args = []

        # AMGX must be built with GCC. This forces the build to use gcc
        # regardless of the compiler environment.
        #
        # Using the environmental gcc/g++ should catch the specific GCC version
        # for GCC compiler environment builds or fall back to the system GCC
        # when in an non-gcc compiler environment.
        #
        # This is potentially a mixed-ABI build when using MPI as the
        # compiler-specific MPI build will be linked into this. For Spectrum-mpi
        # on P9 systems, this should not be a problem as SMPI is delivered via
        # RPM and should be compatible with the system GCC compiler.
        #
        # On other systems, be suspisious of this for complile and runtime
        # errors. Here's to hoping this works.
        if not self.spec.satisfies('%gcc'):
            del env['CPATH']
            args.append('-DCMAKE_C_COMPILER=gcc')
            args.append('-DCMAKE_CXX_COMPILER=g++')

        # Need to force c++11 using gcc-style options.
        args.append('-DCMAKE_CXX_FLAGS=-std=c++11')

        if not self.spec.satisfies('+mpi'):
            args.append('-DCMAKE_NO_MPI:BOOL=True')

        if self.spec.satisfies('+magma'):
            args.append('-DMAGMA_ROOT_DIR:PATH=%s' % self.spec['magma'].prefix)
            if self.spec.satisfies('@2.0.0.130.0'):
                args.append('-DOPENBLAS_ROOT_DIR:PATH=%s' % self.spec['openblas'].prefix)

        if self.spec.satisfies('+openmp'):
            args.append('-DCMAKE_DISABLE_FIND_PACKAGE_OpenMP:BOOL=False')
        else:
            args.append('-DCMAKE_DISABLE_FIND_PACKAGE_OpenMP:BOOL=True')

        return args
