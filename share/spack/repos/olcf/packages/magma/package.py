# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class Magma(CMakePackage):
    """The MAGMA project aims to develop a dense linear algebra library similar to
       LAPACK but for heterogeneous/hybrid architectures, starting with current
       "Multicore+GPU" systems.
    """

    homepage = "http://icl.cs.utk.edu/magma/"
    url = "http://icl.cs.utk.edu/projectsfiles/magma/downloads/magma-2.2.0.tar.gz"
    maintainers = ['luszczek']

    version('2.5.1',
            sha256='ce32c199131515336b30c92a907effe0c441ebc5c5bdb255e4b06b2508de109f',
            preferred=True)
    version('2.5.1-alpha1', sha256='0576ddef07e049e2674fa87caca06ffe96f8d92134ed8aea387b9523be0d7c77')
    version('2.5.0', sha256='4fd45c7e46bd9d9124253e7838bbfb9e6003c64c2c67ffcff02e6c36d2bcfa33')
    version('2.4.0', sha256='4eb839b1295405fd29c8a6f5b4ed578476010bf976af46573f80d1169f1f9a4f')
    version('2.3.0', sha256='010a4a057d7aa1e57b9426bffc0958f3d06913c9151463737e289e67dd9ea608')
    version('2.2.0', sha256='df5d4ace417e5bf52694eae0d91490c6bde4cde1b0da98e8d400c5c3a70d83a2')

    variant('fortran', default=True,
            description='Enable Fortran bindings support')
    variant('shared', default=True,
            description='Enable shared library')

    gpu_targets = ('none', 'kepler', 'fermi', 'maxwell', 'pascal', 'volta')
    variant('gpus', default='none',
            values=gpu_targets,
            multi=True,
            description='Enables support for specific CUDA GPUs.')

    # Version 2.2.0 only supports up to "Maxwell", but not "Volta"
    conflicts('gpus=volta', when='@:2.2.0')

    depends_on('blas')
    depends_on('lapack')
    depends_on('cuda', type=('build', 'run'))

    conflicts('%gcc@6:', when='^cuda@:8')
    conflicts('%gcc@7:', when='^cuda@:9')

    patch('ibm-xl.patch', when='@2.2:2.5.0%xl')
    patch('ibm-xl.patch', when='@2.2:2.5.0%xl_r')
    patch('magma-2.3.0-gcc-4.8.patch', when='@2.3.0%gcc@:4.8')
    patch('magma-2.5.0.patch', when='@2.5.0')
    patch('magma-2.5.0-cmake.patch', when='@2.5.0')

    def cmake_args(self):
        spec = self.spec
        options = []

        if spec.satisfies('+shared'):
            options.extend(['-DBUILD_SHARED_LIBS=ON'])
        else:
            options.append('-DBUILD_SHARED_LIBS=OFF')

        if '+fortran' in spec:
            options.append('-DUSE_FORTRAN=yes')

        gpus = ' '.join([target.capitalize() for target
                         in self.gpu_targets
                         if (target != 'none' and
                             spec.satisfies('gpus=%s' % target))])

        if gpus:
            options.append('-DGPU_TARGET="%s"' % gpus)

        if spec.satisfies('@2.5.0'):
            options.append('-DMAGMA_SPARSE=OFF')
            if spec.compiler.name in ['xl', 'xl_r']:
                options.append('-DCMAKE_DISABLE_FIND_PACKAGE_OpenMP=TRUE')

        return options
