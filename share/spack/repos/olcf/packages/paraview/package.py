# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
from spack.pkg.builtin.paraview import Paraview as ParaviewBase


class Paraview(ParaviewBase):
    """ParaView is an open-source, multi-platform data analysis and
    visualization application."""

    maintainers = ['chuckatkins', 'danlipsa', 'mpbelhorn']

    version('5.6.1', sha256='50ef01f54db6358b402e50d1460ef47c04d675bf26f250c6937737169f1e6612')

    variant('visitbridge', default=True,
            description="Enable the ViSiT DB bridge")
    variant('silo', default=True, description="Enable SILO support.")

    depends_on('boost', when='+visitbridge')
    depends_on('silo+mpi', when='+silo+mpi')
    depends_on('silo~mpi', when='+silo~mpi')

    conflicts('+silo', when='~visitbridge')


    def cmake_args(self):
        spec = self.spec
        cmake_args = super().cmake_args()

        if '+visitbridge' in spec:
            cmake_args.extend([
                '-DPARAVIEW_USE_VISITBRIDGE:BOOL=ON',
                '-DBoost_INCLUDE_DIR:PATH=%s' % spec['boost'].prefix.include,
                ])
            if '+silo' in spec:
                silo_lib = find_libraries(
                    ['libsiloh5', 'libsilo'],
                    root=spec['silo'].prefix.lib,
                    shared=True,
                    recursive=False).libraries[0]
                cmake_args.extend([
                    '-DVISIT_BUILD_READER_Silo:BOOL=ON',
                    '-DSILO_INCLUDE_DIR:FILEPATH=%s' % spec['silo'].prefix.include,
                    # '-DSILO_LIBRARY=%s' % spec['silo'].prefix.lib,
                    '-DSILO_LIBRARY=%s' % silo_lib,
                    ])


        return cmake_args
