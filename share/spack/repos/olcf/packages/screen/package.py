# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Screen(AutotoolsPackage):
    """Screen is a full-screen window manager that multiplexes a physical
    terminal between several processes, typically interactive shells.
    """

    homepage = "https://www.gnu.org/software/screen/"
    url      = "https://ftpmirror.gnu.org/screen/screen-4.3.1.tar.gz"

    version('4.6.2', 'a0f529d3333b128dfaa324d978ba73a8')
    version('4.3.1', '5bb3b0ff2674e29378c31ad3411170ad')
    version('4.3.0', 'f76d28eadc4caaf6cdff00685ae6ad46')
    version('4.2.1', '419a0594e2b25039239af8b90eda7d92')
    version('4.2.0', 'e5199156a8ac863bbf92495a7638b612')
    version('4.0.3', '8506fd205028a96c741e4037de6e3c42')
    version('4.0.2', 'ed68ea9b43d9fba0972cb017a24940a1')
    version('3.9.15', '0dff6fdc3fbbceabf25a43710fbfe75f')
    version('3.9.11', '19572f92404995e7b2dea8117204dd67')
    version('3.9.10', 'bbe271715d1dee038b3cd72d6d2f05fb')
    version('3.9.9', '9a8b1d6c7438c64b884c4f7d7662afdc')
    version('3.9.8', '8ddfebe32c2d45410ce89ea9779bb1cf')
    version('3.9.4', '7de72cd18f7adcdf993ecc6764d0478a')
    version('3.7.6', '9a353b828d79c3c143109265cae663a7')
    version('3.7.4', 'c5ab40b068968075e41e25607dfce543')
    version('3.7.2', '2d6db5de7fb0cf849cc5a6f94203f029')
    version('3.7.1', '27cdd29318446561ef7c966041cbd2c9')

    depends_on('ncurses')

    parallel = False

    patch('mkdir.patch')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make("install")
