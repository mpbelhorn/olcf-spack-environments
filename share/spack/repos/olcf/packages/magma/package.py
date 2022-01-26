# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkg.builtin.magma import Magma as MagmaBase


class Magma(MagmaBase):
    def cmake_args(self):
        options = super(Magma, self).cmake_args()

        if self.spec.satisfies('%nvhpc'):
            options += ['-DCUDA_NVCC_FLAGS=-allow-unsupported-compiler']
        if self.spec.satisfies('%gcc@8: +cuda target=ppc64le'):
            options.append('-DCUDA_NVCC_FLAGS=-Xcompiler;-mno-float128')
        return options
