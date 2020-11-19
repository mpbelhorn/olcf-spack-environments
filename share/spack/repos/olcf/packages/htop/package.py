# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Htop(AutotoolsPackage):
    """htop is an interactive text-mode process viewer for Unix systems."""

    homepage = "https://github.com/htop-dev/htop"
    url      = "https://github.com/htop-dev/htop/archive/2.2.0.tar.gz"
    list_depth = 1

    version('3.0.2', '3295c83198ae764a42627aaa50dd8c90')
    version('2.2.0', '7edaf501e9d117b2acad49bebde9be03')
    version('2.0.2', '7d354d904bad591a931ad57e99fea84a')

    variant('unicode',  default=True,
            description='Enables Unicode character support')

    patch('python2.patch', when='@2.2.0')

    depends_on('ncurses')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    @run_before('autoreconf')
    def make_m4_dir(self):
        m4_dir = join_path(self.build_directory, 'm4')
        if not os.path.exists(m4_dir):
            os.mkdir(m4_dir)

    def configure_args(self):
        options = ['--enable-shared']
        if self.spec.satisfies('+unicode'):
            options.append('--enable-unicode')
        else:
            options.append('--disable-unicode')

        return options
