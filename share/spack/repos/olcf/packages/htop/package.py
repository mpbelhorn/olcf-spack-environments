# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Htop(AutotoolsPackage):
    """htop is an interactive text-mode process viewer for Unix systems."""

    homepage = "https://github.com/hishamhm/htop"
    url      = "https://hisham.hm/htop/releases/2.0.2/htop-2.0.2.tar.gz"
    list_url = "https://hisham.hm/htop/releases"
    list_depth = 1

    version('2.2.0', '0d816b6beed31edc75babcfbf863ffa8')
    version('2.0.2', '7d354d904bad591a931ad57e99fea84a')

    variant('unicode',  default=True,
            description='Enables Unicode character support')

    patch('python2.patch', when='@2.2.0')

    depends_on('ncurses')

    def configure_args(self):
        options = ['--enable-shared']
        if self.spec.satisfies('+unicode'):
            options.append('--enable-unicode')
        else:
            options.append('--disable-unicode')

        return options
