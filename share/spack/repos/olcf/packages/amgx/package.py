# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
 

from spack import *
from spack.pkg.builtin.amgx import Amgx as AmgxBase


class Amgx(AmgxBase):
    """AmgX provides a simple path to accelerated core solver technology on
    NVIDIA GPUs. AmgX provides up to 10x acceleration to the computationally
    intense linear solver portion of simulations, and is especially well
    suited for implicit unstructured methods. It is a high performance,
    state-of-the-art library and includes a flexible solver composition
    system that allows a user to easily construct complex nested solvers and
    preconditioners."""

    git = 'https://github.com/NVIDIA/AMGX.git'

    version('2.1.0-1', commit='11af85608ea0f4720e03cbcc920521745f9e40e5')

    def cmake_args(self):
        args = super().cmake_args()
        spec = self.spec

        if self.spec.satisfies('%gcc target=ppc64le'):
            args.append('-DCUDA_NVCC_FLAGS=-Xcompiler=-mno-float128;-Xcompiler=-fPIC')

        args.append("-DCMAKE_DISABLE_FIND_PACKAGE_OpenMP={0}".format(
            '0' if spec.satisfies('+openmp') else '1'))


        return args
