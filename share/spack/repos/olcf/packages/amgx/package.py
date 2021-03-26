# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkg.builtin.amgx import Amgx as AmgxBase

class Amgx(AmgxBase):
    git = 'https://github.com/NVIDIA/AMGX.git'

    maintainers = ['js947', 'mpbelhorn']

    version('2.1.0-1', commit='11af85608ea0f4720e03cbcc920521745f9e40e5')
    version('2.1.0', sha256='6245112b768a1dc3486b2b3c049342e232eb6281a6021fffa8b20c11631f63cc')
    version('2.0.1', sha256='6f9991f1836fbf4ba2114ce9f49febd0edc069a24f533bd94fd9aa9be72435a7')
    version('2.0.0', sha256='8ec7ea8412be3de216fcf7243c4e2a8bcf76878e6865468e4238630a082a431b')

    variant('openmp', default=True, description='Build with OpenMP support')

    def cmake_args(self):
        args = super(Amgx, self).cmake_args()
        spec = self.spec

        if self.spec.satisfies('%gcc@8: +cuda target=ppc64le'):
            args.append('-DCUDA_NVCC_FLAGS=-Xcompiler=-mno-float128;-Xcompiler=-fPIC')

        args.append("-DCMAKE_DISABLE_FIND_PACKAGE_OpenMP={0}".format(
            '0' if spec.satisfies('+openmp') else '1'))

        return args
