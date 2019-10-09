##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install icewm
#
# You can edit this file again by typing:
#
#     spack edit icewm
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Icewm(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/bbidulock/icewm/archive/1.4.2.tar.gz"

    version('1.4.2',       'db9900056366adc163b2e501a5247bbc')
    version('1.4.1',       '4fbcc936943763a90d6740f8fb4f77c2')
    version('1.4.0',       'd49213506c3bf27c0727935ba6fb0282')
    version('1.3.12',      'ab4671878fc36d5f96896a04e5f8c0bc')
    version('1.3.11',      '60e8514e9b065bcce7f05e0ac5bad334')
    version('1.3.10',      '9e3b77c930a34304f1e1b5ec0685df25')
    version('1.3.9',       '61e3ee7b8b269733485b2a9b646e7b95')
    version('1.3.8',       '8e1c9cde7dfe21d6c71f9e26b09d0268')
    version('icewm_1_3_8', '967f22ec45e8e3b05eb8db1b88e6b6ce')

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    #depends_on('libxft')
    depends_on('libxinerama')
    depends_on('libxpm')
    depends_on('libjpeg')
    depends_on('libxrandr')
    depends_on('python')
    depends_on('asciidoc', type='build')

    def configure_args(self):
        args = []
        args.append('--prefix=%s' % self.prefix)
        args.append('--sysconfdir=/etc')
        args.append('--disable-xfreetype')
        args.append('--enable-corefonts')
        args.append('--without-doc')
        return args

    def install(self, spec, prefix):
        autogen = Executable('./autogen.sh')
        autogen()
        configure(*self.configure_args())
        make()
        make('install')
